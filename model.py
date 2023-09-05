import pydantic
from datetime import datetime
from typing import Generic, Tuple, List, Dict, TypeVar, Type
from pydantic import BaseModel, Field, PositiveInt, model_serializer, RootModel
from uuid import UUID, uuid4
from pathlib import Path
from rich.console import Console

console = Console()

T = TypeVar("T")

# Used as a type annotation anywhere we want a 'base' object
M = TypeVar("M", bound="Base")
Id = int
Collection = Dict[Id, M]


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


def create_collection(*items: M) -> Collection[M]:
    coll = {}
    for item in items:
        console.print(item)
        coll[item.id] = item
    return coll


class Model(Base):
    locations: Collection[Location] = Field(..., default_factory=dict)
    routes: Collection[Route] = Field(..., default_factory=dict)
    ships: Collection[Ship] = Field(..., default_factory=dict)
    assignments : Collection[RouteAssignment] = Field(...,default_factory=dict)


def save_model(model: M, path) -> Path:
    """
    Write the given model to json
    """
    path = Path(path)
    json = model.model_dump_json()
    path.write_text(json)
    console.print(f"Wrote {model} to {path}")
    return path


def load_model(model_type: Type[M], path) -> Path:
    """
    Read an instance of the given model type from
    the path provided
    """
    path = Path(path)
    json = path.read_text()
    model = model_type.model_validate_json(json)
    console.print(f"Read {model} from {path}")
    return path