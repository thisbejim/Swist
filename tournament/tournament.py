#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches")
    db.commit()
    db.close()



def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players")
    counted = c.fetchone()
    db.close()
    return counted[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # Returns player info, including id, name, wins, and matches played
    c.execute("select players.id, players.name, count(matchResults.winnerId) as wins, count(matches.id) as matchNum "
              "from players left join matches on players.id = matches.playerOneId or players.id = matches.playerTwoId "
              "left join matchResults on players.id = matchResults.winnerId group by players.id order by players.name")
    standing = c.fetchall()
    db.close()
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # Adds players to a new match
    c.execute("insert into matches (playerOneId, playerTwoId) values (%s, %s)", (winner, loser,))
    db.commit()
    # Returns the match id
    c.execute("select id from matches where playerOneId = %s and playerTwoId = %s", (winner, loser,))
    match_id = c.fetchone()
    # Adds result of match
    c.execute("insert into matchResults (winnerId, matchId) values (%s, %s)", (winner, match_id,))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    # Returns players in order of wins
    c.execute("select players.id, players.name, count(matchResults.winnerId) as wins from players left join "
              "matchResults on players.id = matchResults.winnerId group by players.id order by wins desc")
    # Format result
    this_pair = []
    pairs = []
    for i in c.fetchall():
        this_pair.append(i[0])
        this_pair.append(i[1])
        if len(this_pair) == 4:
            this_pair_tuple = tuple(this_pair)
            pairs.append(this_pair_tuple)
            this_pair[:] = []

    db.close()
    return pairs



