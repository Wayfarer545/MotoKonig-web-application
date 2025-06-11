from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location


def test_event_creation_valid():
    organizer_id = uuid4()
    location = Location(latitude=54.71, longitude=20.51, address="Kaliningrad")
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    event = Event(
        organizer_id=organizer_id,
        title="Ride Out",
        description="Group ride to the seaside",
        location=location,
        start_time=start_time,
        end_time=end_time,
        event_type=EventType.PUBLIC,
        max_participants=50,
    )

    assert event.organizer_id == organizer_id
    assert event.title == "Ride Out"
    assert event.description.startswith("Group ride")
    assert event.location == location
    assert event.start_time == start_time
    assert event.end_time == end_time
    assert event.event_type == EventType.PUBLIC
    assert event.max_participants == 50


def test_event_validation_errors():
    location = Location(latitude=54.71, longitude=20.51)
    start = datetime.utcnow() + timedelta(days=1)
    with pytest.raises(ValueError):
        Event(
            organizer_id=uuid4(),
            title="",
            description="desc",
            location=location,
            start_time=start,
        )
    with pytest.raises(ValueError):
        Event(
            organizer_id=uuid4(),
            title="Test",
            description="short",
            location=location,
            start_time=start,
        )
    with pytest.raises(ValueError):
        Event(
            organizer_id=uuid4(),
            title="Test Event",
            description="Long enough description",
            location=location,
            start_time=start,
            end_time=start - timedelta(hours=1),
        )
