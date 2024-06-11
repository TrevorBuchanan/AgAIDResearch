class VIState:
    def __init__(self, vegetation_formula: str, vegetation_index_mean: float):
        self.vegetation_formula: str = vegetation_formula
        self.vegetation_index_mean: float = vegetation_index_mean

    def __repr__(self):
        return (f"VIState(vegetation_formula={self.vegetation_formula}, "
                f"vegetation_index_mean={self.vegetation_index_mean})")
