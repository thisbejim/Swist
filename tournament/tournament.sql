-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Player info
CREATE TABLE players(
id serial PRIMARY KEY,
name text
);

-- Match pairing
CREATE TABLE matches(
id serial PRIMARY KEY,
playerOneId serial references players(id) ON DELETE CASCADE,
playerTwoId serial references players(id) ON DELETE CASCADE
);

-- Match results
CREATE TABLE matchResults(
matchId serial references matches(id) ON DELETE CASCADE,
winnerId serial references players(id) ON DELETE CASCADE
);