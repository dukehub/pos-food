import { computed, watch } from 'vue'
import { useStorage } from '@vueuse/core'
import { useI18n } from 'vue-i18n'

// Global singleton state for persistence
const storedLocale = useStorage('locale', 'fr')

export function useLocaleDirection() {
    const { locale: i18nLocale } = useI18n()

    // Compute direction based on stored locale
    const direction = computed(() => storedLocale.value === 'ar' ? 'rtl' : 'ltr')

    // Update document attributes
    const updateDocumentAttributes = () => {
        if (typeof document === 'undefined') return

        const html = document.documentElement
        html.setAttribute('lang', storedLocale.value)
        html.setAttribute('dir', direction.value)

        // Manage class for easier styling
        html.classList.remove('ltr', 'rtl')
        html.classList.add(direction.value)
    }

    // Initialize and watch for changes
    const initLocaleDirection = () => {
        // Sync i18n with storage on init
        i18nLocale.value = storedLocale.value
        updateDocumentAttributes()

        // Watch for changes to update document and i18n
        watch(storedLocale, (newLocale) => {
            i18nLocale.value = newLocale
            updateDocumentAttributes()
        })
    }

    // Set generic locale setter
    const setLocale = (newLocale: string) => {
        storedLocale.value = newLocale
    }

    return {
        locale: storedLocale,
        direction,
        setLocale,
        initLocaleDirection
    }
}
