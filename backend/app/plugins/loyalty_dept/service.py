from decimal import Decimal
from sqlalchemy import select, func as sa_func

from app.orders.models import Order  # ✅ important
from app.plugins.loyalty_debt.models import CustomerLedgerEntry, CustomerAccount, LedgerEntryType


def D(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x or 0))


def customer_balance(session, tenant_id: str, customer_id: str) -> Decimal:
    total = session.execute(
        select(sa_func.coalesce(sa_func.sum(CustomerLedgerEntry.amount), 0))
        .where(
            CustomerLedgerEntry.tenant_id == tenant_id,
            CustomerLedgerEntry.customer_id == customer_id,
        )
    ).scalar_one()
    return D(total)


def upsert_account_balance(session, tenant_id: str, customer_id: str) -> Decimal:
    bal = customer_balance(session, tenant_id, customer_id)

    acc = session.execute(
        select(CustomerAccount).where(
            CustomerAccount.tenant_id == tenant_id,
            CustomerAccount.customer_id == customer_id,
        )
    ).scalar_one_or_none()

    if acc is None:
        acc = CustomerAccount(tenant_id=tenant_id, customer_id=customer_id, balance=bal)
        session.add(acc)
    else:
        acc.balance = bal

    return bal


def checkout_order_order_first(
    session,
    tenant_id: str,
    order_id: str,
    customer_id: str,
    paid_amount,
    note: str | None = None,
):
    """
    Encaissement sur place (commande d'abord puis dettes).

    paid_amount:
      - peut être 0 (client ne paie rien => toute la commande devient dette)
      - peut être partiel
      - peut dépasser le reste de la commande => le surplus paie les dettes anciennes
    """
    paid_amount = D(paid_amount)

    order: Order = session.execute(
        select(Order).where(Order.tenant_id == tenant_id, Order.id == order_id)
    ).scalar_one()

    # Associer le client à la commande
    if order.customer_id and order.customer_id != customer_id:
        raise ValueError("Order already linked to a different customer")
    order.customer_id = customer_id

    order_total = D(order.total_amount)

    # Reste dû sur la commande (cache)
    already_paid = D(order.amount_paid)
    remaining = max(order_total - already_paid, Decimal("0"))

    # 1) paiement d'abord sur la commande
    paid_to_order = min(paid_amount, remaining)
    if paid_to_order > 0:
        session.add(CustomerLedgerEntry(
            tenant_id=tenant_id,
            customer_id=customer_id,
            order_id=order_id,
            entry_type=LedgerEntryType.PAYMENT,
            amount=-paid_to_order,
            note=note or "Payment for order",
        ))
        order.amount_paid = already_paid + paid_to_order

    remaining = max(order_total - D(order.amount_paid), Decimal("0"))
    order.amount_due = remaining

    # 2) transformer le reste en dette (CHARGE) — sans doublonner
    charged_for_order = session.execute(
        select(sa_func.coalesce(sa_func.sum(CustomerLedgerEntry.amount), 0))
        .where(
            CustomerLedgerEntry.tenant_id == tenant_id,
            CustomerLedgerEntry.customer_id == customer_id,
            CustomerLedgerEntry.order_id == order_id,
            CustomerLedgerEntry.entry_type == LedgerEntryType.CHARGE,
        )
    ).scalar_one()
    charged_for_order = D(charged_for_order)

    delta_charge = remaining - charged_for_order
    if delta_charge > 0:
        session.add(CustomerLedgerEntry(
            tenant_id=tenant_id,
            customer_id=customer_id,
            order_id=order_id,
            entry_type=LedgerEntryType.CHARGE,
            amount=delta_charge,
            note=note or "Charge for unpaid remainder",
        ))

    # 3) surplus => dettes anciennes
    surplus = paid_amount - paid_to_order
    paid_to_debt = Decimal("0")
    if surplus > 0:
        paid_to_debt = surplus
        session.add(CustomerLedgerEntry(
            tenant_id=tenant_id,
            customer_id=customer_id,
            order_id=None,
            entry_type=LedgerEntryType.PAYMENT,
            amount=-paid_to_debt,
            note=note or "Payment for previous debts",
        ))

    # 4) statut
    order.status = "closed" if order.amount_due == 0 else "confirmed"

    # 5) maj solde cache
    new_balance = upsert_account_balance(session, tenant_id, customer_id)

    return {
        "order_total": order_total,
        "paid_to_order": paid_to_order,
        "paid_to_debt": paid_to_debt,
        "order_amount_paid": D(order.amount_paid),
        "order_amount_due": D(order.amount_due),
        "customer_balance": new_balance,
        "order_status": order.status,
    }


def pay_customer_debt_only(session, tenant_id: str, customer_id: str, amount, note: str | None = None):
    amount = D(amount)
    if amount <= 0:
        return {"paid": Decimal("0"), "customer_balance": upsert_account_balance(session, tenant_id, customer_id)}

    session.add(CustomerLedgerEntry(
        tenant_id=tenant_id,
        customer_id=customer_id,
        order_id=None,
        entry_type=LedgerEntryType.PAYMENT,
        amount=-amount,
        note=note or "Debt payment",
    ))

    new_balance = upsert_account_balance(session, tenant_id, customer_id)
    return {"paid": amount, "customer_balance": new_balance}
