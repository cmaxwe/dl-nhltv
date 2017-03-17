import urllib2
import xml.etree.ElementTree as ET


class Team(object):
    fullName = "Detroit Red Wings"
    id = 17
    abbreviation = "DET"

    def __str__(self):
        return str(self.__dict__)


class Teams(object):
    """
    ==================================================
    Get NHL TV Team names
    ==================================================
    Class parses all teams so that you can pull from it.

    Arguments:
        _parseTeam (etree): ElementTree root

    Returns:
        Team: Team object
    """
    team = Team()
    teams = {}
    user_agent = 'PS4Application libhttp/1.000 (PS4) libhttp/3.15 (PlayStation 4)'
    url = 'http://app.cgy.nhl.yinzcam.com/V2/Stats/Standings'

    def getTeam(self, search):
        """
        ==================================================
        Get Team
        ==================================================

        Arguments:
            search (int): by team id number like 17
            search (STR): search by teams TriCode/abbreviation like "DET"
            search (str): search by team name like "Detroit Red Wings"

        Returns:
            Team: Team object
        """
        if len(self.teams) < 3:
            self._fetchTeams()

        if isinstance(search, int):
            return self._searchTeamById(search)
        if search.isdigit():
            return self._searchTeamById(int(search))
        if search.isupper():
            return self._searchTeamByAbbreviation(search)
        return self._searchTeamName(search)

    def _fetchTeams(self):
        req = urllib2.Request(self.url)
        req.add_header('Connection', 'close')
        req.add_header('User-Agent', self.user_agent)
        response = urllib2.urlopen(req)
        xml = response.read().decode('utf-8-sig')
        self._parseGameContentSchedule(ET.fromstring(xml))
        response.close()

    def _parseTeam(self, team):
        t = Team()
        t.fullName = team["Team"]
        t.id = int(team["Id"])
        t.abbreviation = team["TriCode"]
        self.teams[t.abbreviation] = t

    def _parseGameContentSchedule(self, tree):
        for item in tree.iter("Standing"):
            self._parseTeam(item.attrib)

    def _searchTeamByAbbreviation(self, search=str):
        return self.teams[search]

    def _searchTeamById(self, search=int):
        for team in self:
            if search is team.id:
                return team
        raise LookupError('Could not find team with id %s' % search)

    def _searchTeamName(self, search):
        for team in self.teams.values():
            if search in team.fullName:
                return team
        raise LookupError('Could not find team with id %s' % search)

    def __iter__(self):
        return iter(self.teams.values())

    def __len__(self):
        return len(self.teams.items())
