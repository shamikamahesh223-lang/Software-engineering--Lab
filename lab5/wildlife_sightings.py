"""Record and summarize wildlife sightings using SQLite."""

import hashlib
import sqlite3


def create_database():
    """Create the in-memory database and sightings table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE sightings (
            id INTEGER PRIMARY KEY,
            species TEXT,
            zone TEXT,
            count INTEGER
        )
        """
    )
    return connection


def log_sighting(connection, species, zone, count, extras=None):
    """Store a sighting and update cumulative species totals."""
    if extras is None:
        extras = {}

    connection.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count),
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Return a short SHA-256 identifier for an observer."""
    return hashlib.sha256(observer.encode("utf-8")).hexdigest()[:12]


def zone_summary(connection, zone):
    """Return the total number of sightings recorded in a zone."""
    row = connection.execute(
        "SELECT SUM(count) FROM sightings WHERE zone = ?",
        (zone,),
    ).fetchone()

    if row[0] is None:
        return 0
    return row[0]


def rarest(connection):
    """Return the species with the lowest total sighting count."""
    rows = connection.execute(
        """
        SELECT species, SUM(count)
        FROM sightings
        GROUP BY species
        """
    ).fetchall()

    if not rows:
        return None

    least_seen = min(rows, key=lambda row: row[1])
    return least_seen[0]


def main():
    """Run a demonstration of wildlife sightings."""
    connection = create_database()
    totals = log_sighting(connection, "Leopard", "North", 1)
    log_sighting(connection, "Chital", "North", 24, totals)
    log_sighting(connection, "Hornbill", "East", 3, totals)

    if len(totals) != 3:
        raise RuntimeError("Unexpected number of species totals")

    print(
        observer_id("Arun"),
        zone_summary(connection, "North"),
        rarest(connection),
    )
    connection.close()


if __name__ == "__main__":
    main()
