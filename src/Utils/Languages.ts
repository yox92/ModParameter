export class Languages {
    public static readonly serverSupportedLocales: string[] = [
        "ar", "en", "cs", "da", "de", "el", "es-es", "fr", "nl", "no", "tr",
        "hi", "hu", "id", "it", "ja", "ko", "pl", "pt-br", "pt-pt", "ru", "sv", "vi", "zh-cn"
    ];

    public static readonly translations: Record<string, { name: string; shortName: string; description: string }> = {
        "ar": {name: `{name} نسخة`, shortName: `{shortName} نسخة`, description: `{name} نسخة مستنسخة`},
        "en": {name: `{name} Clone`, shortName: `{shortName} Clone`, description: `{name} Cloned version`},
        "cs": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Klonovaná verze`},
        "da": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Klonet version`},
        "de": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Geklonte Version`},
        "el": {name: `{name} Κλώνος`, shortName: `{shortName} Κλώνος`, description: `{name} Κλωνοποιημένη έκδοση`},
        "es-es": {name: `{name} Clon`, shortName: `{shortName} Clon`, description: `{name} Versión clonada`},
        "fr": {name: `{name} Clone`, shortName: `{shortName} Clone`, description: `{name} Version clonée`},
        "nl": {name: `{name} Kloon`, shortName: `{shortName} Kloon`, description: `{name} Gekloonde versie`},
        "no": {name: `{name} Klone`, shortName: `{shortName} Klone`, description: `{name} Klonet versjon`},
        "tr": {name: `{name} Klonu`, shortName: `{shortName} Klon`, description: `{name} klonlanmış sürümü`},
        "hi": {name: `{name} क्लोन`, shortName: `{shortName} क्लोन`, description: `{name} का क्लोन संस्करण`},
        "hu": {name: `{name} Klón`, shortName: `{shortName} Klón`, description: `{name} klónozott verziója`},
        "id": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Versi klon`},
        "it": {name: `{name} Clone`, shortName: `{shortName} Clone`, description: `{name} Versione clonata`},
        "ja": {name: `{name} クローン`, shortName: `{shortName} クローン`, description: `{name} のクローンバージョン`},
        "ko": {name: `{name} 클론`, shortName: `{shortName} 클론`, description: `{name} 의 복제 버전`},
        "pl": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Sklonowana wersja`},
        "pt-br": {name: `{name} Clone`, shortName: `{shortName} Clone`, description: `{name} Versão clonada`},
        "pt-pt": {name: `{name} Clone`, shortName: `{shortName} Clone`, description: `{name} Versão clonada`},
        "ru": {name: `{name} Клон`, shortName: `{shortName} Клон`, description: `{name} Клонированная версия`},
        "sv": {name: `{name} Klon`, shortName: `{shortName} Klon`, description: `{name} Klonad version`},
        "vi": {name: `{name} Bản sao`, shortName: `{shortName} Bản sao`, description: `{name} Phiên bản sao chép`},
        "zh-cn": {name: `{name} 克隆`, shortName: `{shortName} 克隆`, description: `{name} 的克隆版本`}
    };

    /**
     * Generates locales for a given item
     * @param name Original item's name
     * @param shortName Original item's short name
     * @returns An object containing translations in all supported languages
     */
    public static generateLocales(name: string, shortName: string): Record<string, any> {
        const locales: Record<string, any> = {};

        this.serverSupportedLocales.forEach(lang => {
            const translation = this.translations[lang] || this.translations["en"];

            locales[lang] = {
                name: translation.name.replace("{name}", name).replace("{shortName}", shortName),
                shortName: translation.shortName.replace("{name}", name).replace("{shortName}", shortName),
                description: translation.description.replace("{name}", name).replace("{shortName}", shortName)
            };
        });

        return locales;
    }
}


