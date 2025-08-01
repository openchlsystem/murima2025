import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import fr from '@/locales/fr.json'

const i18n = createI18n({
    legacy: false,
    locale: 'en',          // Default locale
    fallbackLocale: 'en',  // Fallback if key is missing
    messages: {
        en,
        fr
    }
})

export default i18n
