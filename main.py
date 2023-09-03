"""
A demo of using pydantic to declare
a simple data model along with inheritance
and se/deserialization
"""

import pydantic
from datetime import datetime
from typing import Tuple, List, Dict, TypeVar
from pydantic import BaseModel, Field, PositiveInt
from uuid import UUID, uuid4

T = TypeVar("T")
Id = TypeVar("Id", bound=int)
Collection = Dict[int, T]

MAX_ID = 0
def new_id():
    """
    Create a new ID - production would probably use `UUID`
    """
    global MAX_ID
    MAX_ID += 1
    return MAX_ID


class Base(BaseModel):
    """
    We can declare our own base type for all
    other model classes to inherit from.
    In this example we want to enforce that
    everything in our model has both a `id`
    and a `name`
    """
    id: Id = Field(default_factory=new_id)
    name: str = Field(default="")

    def __str__(self):
        return self.name


class Location(Base):
    longitude : float
    latitude : float


class Route(Base):
    origin_location_id : Id
    destination_location_id : Id
    location_ids : List[Id]


class Ship(Base):
    length : float
    weight : float    


class RouteAssignment(Base):
    ship_id : Id
    route_id : Id
    
    def __str__(self):
        return f"Ship {self.ship_id} on Route {self.route_id}"


class Model(Base):
    locations: Collection[Location]
    routes: Collection[Route]
    ships: Collection[Ship]
    assignments : Collection[RouteAssignment]


# =========================================================
def collection(*args):
    return {arg.id : arg for arg in args}

# Create dummy locations
loc_a = Location(name = "Loc A", longitude=43.5, latitude=120.1)
loc_b = Location(name = "Loc B", longitude=44.5, latitude=125.1)
loc_c = Location(name = "Loc C", longitude=45.5, latitude=122.1)
loc_d = Location(name = "Loc D", longitude=46.5, latitude=121.1)
locations = collection(loc_a, loc_b, loc_c, loc_d)

# Create dummy ships
ship_a = Ship(name = "Ship A", weight=1000, length=100)
ship_b = Ship(name = "Ship B", weight=2000, length=122.3)
ships = collection(ship_a, ship_b)

# Create dummy routes
def make_route(name, *locations):
    loc_ids = [loc.id for loc in locations]
    org_id = loc_ids[0]
    dst_id = loc_ids[-1]
    return Route(name=name, origin_location_id=org_id, destination_location_id=dst_id, location_ids=loc_ids)

route_a = make_route("Route A", loc_a, loc_b, loc_d)
route_b = make_route("Route B", loc_a, loc_c, loc_d)
route_c = make_route("Route B", loc_a, loc_d)
routes = collection(route_a, route_b, route_c)

# Create dummy assignments
def assign(ship: Ship, route: Route) -> RouteAssignment:
    return RouteAssignment(name = f"{ship.name} on {route.name}", ship_id=ship.id, route_id=route.id)

assignments = collection(
    assign(ship_a, route_a),
    assign(ship_b, route_c),
    assign(ship_b, route_b)
)

# Create sample model
model1 = Model(name = "Sample Model",
              locations = locations,
              routes = routes,
              ships = ships,
              assignments=assignments)


# Write the model to dict/json
model1_dict = model1.model_dump()
model1_json = model1.model_dump_json()

# Read from json (this will be a deepcopy)
model2 = Model.model_validate_json(model1_json)
model2.name = "Model 2"

# Read from dict (this will probably share references so be careful)
model3 = Model.model_validate(model1_dict)
model3.name = "Model 3"

# Use the inbuilt copy method (best idea)
model4 = model1.model_copy(update=dict(name="Model 4"), deep=True)
