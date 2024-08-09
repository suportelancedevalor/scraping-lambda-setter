from features.mega_leilao.gateway.presenter import Presenter

class GatewayInjector:
    self = None

    def __init__(self):
        pass

    @property
    def presenter(self) -> Presenter:
        if self.self is None:
            raise RuntimeError("GatewayInjector.self not initialized")
        return self.self.presenter
