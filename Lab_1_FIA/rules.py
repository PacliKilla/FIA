from production import IF, AND, THEN

RULES = (

    IF(AND('(?y) has unerdaged',  # kid
           '(?y) has education',
           '(?y) has onesie',
           '(?y) has socks',
           '(?y) has parents'),
       THEN('(?y) is a Kid')),

    IF(AND('(?y) has bachelor',  # adult
           '(?y) has married',
           '(?y) has suit',
           '(?y) has stylish'),
       THEN('(?y) is a Adult')),

    IF(AND('(?y) has bachelor',  # middle age
           '(?y) has married',
           '(?y) has hat',
           '(?y) has stylish'),
       THEN('(?y) is a Middle_age')),

    IF(AND('(?y) has bachelor',  # geezer
           '(?y) has married',
           '(?y) has suit',
           '(?y) has hat'),
       THEN('(?y) is a Geezer')),

    IF(AND('(?y) has unerdaged',  # teen
           '(?y) has education',
           '(?y) has onesie',
           '(?y) has beard',
           '(?y) has parents'),
       THEN('(?y) is a Teen')),
)


class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)


tree = Tree('{0} has unerdaged',
            Tree('{0} has education', Tree('{0} has onesie',
                                           Tree('{0} has socks', Tree('{0} has parents'),
                                                                   Tree('{0} has beard',
                                                                   Tree('{0} has parents'))))),

            Tree('{0} has bachelor', Tree('{0} has married',

                                          Tree('{0} has suit',
                                               Tree('{0} has stylish',
                                               Tree('{0} has hat'),
                                               Tree('{0} has hat',
                                                    Tree('{0} has stylish')))))))
