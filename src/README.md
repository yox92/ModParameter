DatabaseServer
├── templates
│   ├── items                
│   │   ├── weapon_XXX      <-- Exemple d'une arme
│   │   │   ├── _id: string
│   │   │   ├── _name: string
│   │   │   ├── _props: ItemProps
│   │   │   │   ├── CameraSnap: number
│   │   │   │   ├── AimSensitivity: number
│   │   │   │   ├── Ergonomics: number
│   │   │   │   ├── RecoilCamera: number
│   │   │   │   ├── RecoilForceBack: number
│   │   │   │   ├── RecoilForceUp: number
│   │   │   │   ├── RecolDispersion: number
│   │   │   │   ├── Weight: number
│   │   │   │   ├── ammoCaliber: string
│   │   │   │   ├── bFirerate: number
│   │   ├── ammo_XXX        <-- Exemple d'une munition
│   │   │   ├── _id: string
│   │   │   ├── _name: string
│   │   │   ├── _props: Ammo
│   │   │   │   ├── ArmorDamage: number
│   │   │   │   ├── Caliber: string
│   │   │   │   ├── Damage: number
│   │   │   │   ├── InitialSpeed: number
│   │   │   │   ├── PenetrationPower: number
│   │   │   │   ├── StackMaxSize: number
│   │   │   │   ├── Tracer: boolean
│   │   │   │   ├── TracerColor: string
├── globals
│   ├── config
│   │   ├── Aiming
│   │   │   ├── AimPunchMagnitude: number
│   │   │   ├── RecoilDamping: number
│   │   │   ├── RecoilHandDamping: number
│   │   │   ├── RecoilIntensityStanding: number
│   │   │   ├── RecoilIntensityCrouching: number
│   │   │   ├── RecoilIntensityProne: number
│   │   │   ├── RecoilXIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number
│   │   │   ├── RecoilYIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number
│   │   │   ├── RecoilZIntensityByPose
│   │   │   │   ├── x: number
│   │   │   │   ├── y: number
│   │   │   │   ├── z: number
