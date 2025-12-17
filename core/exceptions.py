class OkssangimongError(Exception):
    """Base error for domain."""


class AddressNotFoundError(OkssangimongError):
    pass


class BuildingNotFoundError(OkssangimongError):
    pass


class RooftopAreaUnavailableError(OkssangimongError):
    pass


class InvalidScenarioError(OkssangimongError):
    pass
