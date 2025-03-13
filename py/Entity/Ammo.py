from Entity.EnumAmmo import EnumAmmo


class Ammo:
    def __init__(self, **props):
        self._ArmorDamage = (
            props.get(EnumAmmo.ARMOR_DAMAGE.label, None),
            EnumAmmo.ARMOR_DAMAGE.label
        )
        self._Caliber = (
            props.get(EnumAmmo.CALIBER.label, None),
            EnumAmmo.CALIBER.label
        )
        self._Damage = (
            props.get(EnumAmmo.DAMAGE.label, None),
            EnumAmmo.DAMAGE.label
        )
        self._PenetrationPower = (
            props.get(EnumAmmo.PENETRATION_POWER.label, None),
            EnumAmmo.PENETRATION_POWER.label
        )
        self._StackMaxSize = (
            props.get(EnumAmmo.STACK_MAX_SIZE.label, None),
            EnumAmmo.STACK_MAX_SIZE.label
        )
        self._Tracer = (
            props.get(EnumAmmo.TRACER.label, None),
            EnumAmmo.TRACER.label
        )
        self._TracerColor = (
            self.convert_to_boolean(props.get(EnumAmmo.TRACERCOLOR.label, None)),
            EnumAmmo.TRACERCOLOR.label
        )
        self._InitialSpeed = (
            props.get(EnumAmmo.INITIAL_SPEED.label, None),
            EnumAmmo.INITIAL_SPEED.label
        )
        self._BallisticCoeficient = (
            props.get(EnumAmmo.BALLISTIC_COEFICIENT.label, None),
            EnumAmmo.BALLISTIC_COEFICIENT.label
        )
        self._BulletMassGram = (
            props.get(EnumAmmo.BULLET_MASSGRAM.label, None),
            EnumAmmo.BULLET_MASSGRAM.label
        )
        self._ProjectileCount = (
            props.get(EnumAmmo.PROJECTILE_COUNT.label, None),
            EnumAmmo.PROJECTILE_COUNT.label
        )
        self._ammoAccr = (
            props.get(EnumAmmo.AMMO_ACCR.label, None),
            EnumAmmo.AMMO_ACCR.label
        )
        self._ammoRec = (
            props.get(EnumAmmo.AMMO_REC.label, None),
            EnumAmmo.AMMO_REC.label
        )

    def convert_to_boolean(self, value):
        if isinstance(value, str):
            value = value.strip().lower()
            return value != "red"
        return bool(value)

    @property
    def ArmorDamage(self):
        return self._ArmorDamage

    @property
    def Caliber(self):
        return self._Caliber

    @property
    def Damage(self):
        return self._Damage

    @property
    def InitialSpeed(self):
        return self._InitialSpeed

    @property
    def PenetrationPower(self):
        return self._PenetrationPower

    @property
    def StackMaxSize(self):
        return self._StackMaxSize

    @property
    def Tracer(self):
        return self._Tracer

    @property
    def TracerColor(self):
        return self._TracerColor

    @property
    def BallisticCoeficient(self):
        return self._BallisticCoeficient

    @property
    def BulletMassGram(self):
        return self._BulletMassGram

    @property
    def ProjectileCount(self):
        return self._ProjectileCount

    @property
    def ammoAccr(self):
        return self._ammoAccr

    @property
    def ammoRec(self):
        return self._ammoRec

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

    def get_instance_attributes(self):
        return vars(self)

    def get_attribute_value(self, attr_name):
        return getattr(self, attr_name, None)

    def get_value_by_label(self, label):
        for attr_name in self.get_instance_attributes():
            attr_value = self.get_attribute_value(attr_name)
            if isinstance(attr_value, tuple) and len(attr_value) == 2:
                numeric_value, attr_label = attr_value
                if attr_label == label:
                    return numeric_value
        raise ValueError(f"Le label '{label}' n'a pas été trouvé dans Ammo.")

    def __repr__(self):
        return (f"Ammo("
                f"ArmorDamage={self.ArmorDamage}, "
                f"Caliber={self.Caliber}, "
                f"Damage={self.Damage}, "
                f"InitialSpeed={self.InitialSpeed}, "
                f"PenetrationPower={self.PenetrationPower}, "
                f"StackMaxSize={self.StackMaxSize}, "
                f"Tracer={self.Tracer}), "
                f"BallisticCoeficient={self.BallisticCoeficient}), "
                f"BulletMassGram={self.BulletMassGram}), "
                f"ProjectileCount={self.ProjectileCount}), "
                f"ammoAccr={self.ammoAccr}), "
                f"ammoRec={self.ammoRec}), "
                f"TracerColor={self.TracerColor})")

    def __iter__(self):
        return (key for key in self.__dict__.keys())
