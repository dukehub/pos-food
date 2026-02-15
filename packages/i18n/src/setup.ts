import { createI18n } from 'vue-i18n'
import type { I18n } from 'vue-i18n'
import fr from './locales/fr.json'
import ar from './locales/ar.json'
import en from './locales/en.json'

export type SupportedLocale = 'fr' | 'ar' | 'en'

/** RTL locales */
const RTL_LOCALES: SupportedLocale[] = ['ar']

/**
 * Create a vue-i18n instance pre-loaded with core messages.
 * Each app calls this once in main.ts.
 */
export function createAppI18n(
  appMessages?: Record<string, Record<string, unknown>>
): I18n {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const messages: Record<string, any> = {
    fr: { ...fr },
    ar: { ...ar },
    en: { ...en }
  }

  // Merge app-specific messages
  if (appMessages) {
    for (const [locale, msgs] of Object.entries(appMessages)) {
      if (messages[locale]) {
        Object.assign(messages[locale], msgs)
      } else {
        messages[locale] = { ...msgs }
      }
    }
  }

  const i18n = createI18n({
    legacy: false,
    locale: 'fr',
    fallbackLocale: 'en',
    messages
  })

  // Apply RTL direction on the document — locale type depends on legacy mode
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const loc = (i18n.global as any).locale
  const localeStr: string = typeof loc === 'object' && loc.value ? loc.value : loc
  updateDirection(localeStr as SupportedLocale)

  return i18n
}

/**
 * Merge plugin locale messages into a running i18n instance.
 */
export function mergePluginMessages(
  i18n: I18n,
  pluginMessages: Record<string, Record<string, unknown>>
): void {
  for (const [locale, messages] of Object.entries(pluginMessages)) {
    i18n.global.mergeLocaleMessage(locale, messages)
  }
}

/**
 * Update the document direction (LTR/RTL) based on locale.
 */
export function updateDirection(locale: SupportedLocale): void {
  if (typeof document !== 'undefined') {
    const dir = RTL_LOCALES.includes(locale) ? 'rtl' : 'ltr'
    document.documentElement.setAttribute('dir', dir)
    document.documentElement.setAttribute('lang', locale)
  }
}
