from Entity.EnumBagSize import EnumBagSize


class Bag:
    def __init__(  self,
        ids: str,
        name: str,
        Grids: dict):
        self._ids: str = ids
        self._name: str = name
        self._Grids: dict = Grids

    @property
    def ids(self) -> str:
        return self._ids

    @property
    def name(self) -> str:
        return self._name

    @property
    def Grids(self) -> dict:
        return self._Grids

    def resize_backpacks(self, percent: int):
        import math
        # Get the current grids of the bag
        old_grids = self._Grids
        # Calculate the current total size (sum of all cells)
        total_old_size = sum(g["cellsH"] * g["cellsV"] for g in old_grids.values())
        # Determine the target total size based on the percentage increase
        target_total_size = round(total_old_size * (1 + percent / 100))
        # Prepare a new grid structure to hold resized values
        new_grids = {}
        actual_new_total = 0
        # Resize each grid proportionally to its contribution in the total size
        for gid, grid in old_grids.items():
            current_size = grid["cellsH"] * grid["cellsV"]
            # Handle empty grids (0 cells) by defaulting to 1x1
            if current_size == 0:
                new_grids[gid] = {"cellsH": 1, "cellsV": 1}
                actual_new_total += 1
                continue
            # Calculate the target size for this specific grid
            grid_target_size = (current_size / total_old_size) * target_total_size
            # Compute the scale factor using square root to evenly increase width and height
            scale = math.sqrt(grid_target_size / current_size)
            # Apply the scale to cellsH and cellsV, rounding and enforcing a minimum of 1
            new_H = max(1, round(grid["cellsH"] * scale))
            new_V = max(1, round(grid["cellsV"] * scale))

            if new_H > 7:
                new_H = 7
                # Ajuster V pour compenser et maintenir la surface
                new_V = max(1, round(grid_target_size / new_H))

            new_grids[gid] = {"cellsH": new_H, "cellsV": new_V}
            actual_new_total += new_H * new_V

        self._Grids = new_grids

    def display_resize_info(self, old_grids: dict = None, verbose: bool = False):
        def compute_size(grids):
            return sum(g["cellsH"] * g["cellsV"] for g in grids.values())

        current_size = compute_size(self._Grids)

        if old_grids:
            old_size = compute_size(old_grids)
            print(f"{self._name} name")
            print(f"   Before  : {old_size} slot")
            print(f"   After  : {current_size} slot  (+{round(((current_size - old_size) / old_size) * 100)}%)")
            if verbose:
                print("   Per Grids :")
                for gid in self._Grids:
                    old = old_grids[gid]
                    new = self._Grids[gid]
                    print(f"     - Grid {gid}: {old['cellsH']}x{old['cellsV']} → {new['cellsH']}x{new['cellsV']}")
        else:
            print(f" {self._name} → {current_size} cases (size now)")
