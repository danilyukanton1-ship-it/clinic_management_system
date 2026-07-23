import pytest
from unittest.mock import AsyncMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException, \
    AppointmentRelatesToDifferentPatientException
from app.users.exceptions.user import UserNotFoundException

