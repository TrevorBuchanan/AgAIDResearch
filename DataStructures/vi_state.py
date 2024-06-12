class VIState:
    def __init__(self, vi_formula: str, vi_mean: float):
        self.vi_formula: str = vi_formula
        self.vi_mean: float = vi_mean

    def __repr__(self):
        return (f"VIState(vegetation_formula={self.vi_formula}, "
                f"vegetation_index_mean={self.vi_mean})")
