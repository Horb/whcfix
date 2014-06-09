
import adapters

a = adapters.YorkshireHockeyAssociationAdapter(138, 66, 'Mens')

matches = a.GetMatches()
print set([match for match in matches if match.doesFeature('Wakefield 6 Mens')])
