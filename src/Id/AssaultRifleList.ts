export class AssaultRifleList {
    private ids: string[];

    constructor() {
        this.ids = [
            "6499849fc93611967b034949",
            "5ac66d015acfc400180ae6e4",
            "5ac66d2e5acfc43b321d4b53",
            "5ac66d725acfc43b321d4b60",
            "5ac66d9b5acfc4001633997a",
            "5bf3e03b0db834001d2c4a9c",
            "5ac4cd105acfc40016339859",
            "5644bd2b4bdc2d3b4c8b4572",
            "59d6088586f774275f37482f",
            "5a0ec13bfcdbcb00165aa685",
            "59ff346386f77477562ff5e2",
            "5abcbc27d8ce8700182eceeb",
            "5bf3e0490db83400196199af",
            "5ab8e9fcd8ce870019439434",
            "57dc2fa62459775949412633",
            "5839a40f24597726f856b511",
            "583990e32459771419544dd2",
            "57c44b372459772d2b39b8ce",
            "5cadfbf7ae92152ac412eeef",
            "62e7c4fba689e8c9c50dfc38",
            "63171672192e68c5460cebc5",
            "5c488a752e221602b412af63",
            "5dcbd56fdbd3d91b3e5468d5",
            "5bb2475ed4351e00853264e3",
            "623063e994fc3f7b302a9696",
            "5447a9cd4bdc2dbd208b4567",
            "5fbcc1d9016cce60e8341ab3",
            "606587252535c57a13424cfd",
            "628a60ae6b1d481ff772e9c8",
            "5b0bbe4e5acfc40dc528a72d",
            "6183afd850224f204c1da514",
            "6165ac306ef05c2ce828ef74",
            "6184055050224f204c1da540",
            "618428466ef05c2ce828f218"
        ];
    }

    getIds(): string[] {
        return this.ids;
    }
}

// Usage
const rifleList = new AssaultRifleList();
console.log(rifleList.getIds());
