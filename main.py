from model import *
from rich import print_json

def create_route_assignment(ship: Ship, route: Route) -> RouteAssignment:
    """
    Createa a new route assignment
    """
    return RouteAssignment(name = f"{ship.name} on {route.name}", ship_id=ship.id, route_id=route.id)

def create_route(name: str, *locations: Location):
    """
    Create a new route from the given locations
    """
    loc_ids = [loc.id for loc in locations]
    org_id = loc_ids[0]
    dst_id = loc_ids[-1]
    return Route(name=name, origin_location_id=org_id, destination_location_id=dst_id, location_ids=loc_ids)

if __name__ == "__main__":

    console.print("Creating locations")
    loc_a = Location(name = "Loc A", longitude=43.5, latitude=120.1)
    loc_b = Location(name = "Loc B", longitude=44.5, latitude=125.1)
    loc_c = Location(name = "Loc C", longitude=45.5, latitude=122.1)
    loc_d = Location(name = "Loc D", longitude=46.5, latitude=121.1)
    locations = create_collection(loc_a, loc_b, loc_c, loc_d)
    console.rule()

    print("Creating ships")
    ship_a = Ship(name = "Ship A", weight=1000, length=100)
    ship_b = Ship(name = "Ship B", weight=2000, length=122.3)
    ships = create_collection(ship_a, ship_b)
    console.rule()

    print("Creating routes")
    route_a = create_route("Route A", loc_a, loc_b, loc_d)
    route_b = create_route("Route B", loc_a, loc_c, loc_d)
    route_c = create_route("Route B", loc_a, loc_d)
    routes = create_collection(route_a, route_b, route_c)
    console.rule()

    print("Creating route assignments")
    assignments = create_collection(
        create_route_assignment(ship_a, route_a),
        create_route_assignment(ship_b, route_c),
        create_route_assignment(ship_b, route_b)
    )
    console.rule()
    
    print("Creating model")
    model1 = Model(
        name = "Sample Model",
        locations = locations,
        routes = routes,
        ships = ships,
        assignments = assignments)
    console.print(model1)
    console.rule()

    # Write the model to dictionary using builtin method
    model1_dict = model1.model_dump()

    # Write the model to json string using builtin method
    console.print("Encoding as json")
    model1_json = model1.model_dump_json()
    print_json(model1_json)
    console.rule()
    
    # Create a new model from json string (will be a deepcopy)
    model2 = Model.model_validate_json(model1_json)
    model2.name = "Model 2"

    # Create a new model from a dict (may share references)
    model3 = Model.model_validate(model1_dict)
    model3.name = "Model 3"

    # Copy the model using builtin method
    model4 = model1.model_copy(update=dict(name="Model 4"), deep=True)

    # Roundtrip to json file using our helper methods
    path = save_model(model1, "./model.json")
    model5 = load_model(Model, path)