__author__ = 'ievans3024'


class Database(object):
    """Database wrapper, base class"""

    def __init__(self, app):
        """Constructor for Database"""
        self.app = app
        self.database = {}
        self.models = {}

    def new(self):
        pass

    def edit(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def generate_test_db(self):
        pass

test_first_names = [
    'Alex', 'Andrea', 'Bryce', 'Brianna', 'Cole', 'Cathy', 'Derek', 'Danielle', 'Eric', 'Edith', 'Fred', 'Felicia',
    'Garrett', 'Gianna', 'Harold', 'Helga', 'Ira', 'Ingrid', 'Jonathan', 'Jacquelyn', 'Kerry', 'Karen', 'Larry',
    'Laura', 'Melvin', 'Margaret', 'Noel', 'Natalie', 'Otis', 'Olga', 'Peter', 'Pia', 'Quentin', 'Quinn',
    'Reginald', 'Rachel', 'Steven', 'Samantha', 'Tyler', 'Tullia', 'Ulric', 'Uma', 'Vincent', 'Valerie', 'Wade',
    'Wendy', 'Xavier', 'Xandra', 'Yusef', 'Yolanda', 'Zach', 'Zoe'
]

test_last_names = [
    'Ashford', 'Aldred', 'Beckett', 'Blackford', 'Carey', 'Conaway', 'Delung', 'Doohan', 'Eagan', 'Eastman',
    'Farley', 'Flores', 'Gandy', 'Grimes', 'Harkness', 'Hughley', 'Inman', 'Isley', 'Jager', 'Johannsen',
    'Keatinge', 'Kaufman', 'Lachance', 'Lopez', 'Markley', 'Meeker', 'Norrell', 'Nunnelly', 'Oberman', 'Osmond',
    'Puterbough', 'Pinkman', 'Quigly', 'Quayle', 'Romero', 'Rosenkranz', 'Smith', 'Stillman', 'Titsworth',
    'Thomson', 'Umbrell', 'Underwood', 'Valentine', 'Voyer', 'Wheatley', 'Wetzel', 'Xerxes', 'Xin', 'Yancey',
    'York', 'Zeeley', 'Zorn'
]

test_phone_numbers = [
    '6310', '2686', '8370', '7294', '0480', '8213', '1676', '5981', '9820', '9213', '6547', '1629', '7464', '6742',
    '2307', '3152', '3245', '4283', '0144', '4995', '1271', '9220', '9827', '7032', '4855', '7975', '3912', '8340',
    '7934', '4647', '6552', '3079', '6161', '1307', '3158', '1034', '0295', '2317', '7179', '0743', '8588', '7068',
    '2450', '9826', '6458', '0554', '5614', '5106', '5020', '0577', '7277', '6371'
]

test_address_line1s = [
    '907 23rd St.', '972 24th Ave.', '483 24th Ave.', '676 8th Ave.', '984 21st St.', '923 19th St.',
    '734 13th Ave.', '741 22nd Ave.', '45 20th Ave.', '597 16th St.', '259 15th Ave.', '361 3rd Ave.',
    '697 21st St.', '887 18th Ave.', '403 9th Ave.', '684 9th Ave.', '641 19th Ave.', '398 2nd Ave.',
    '752 11th St.', '237 14th St.', '393 8th Ave.', '603 18th Ave.', '601 15th St.', '54 2nd Ave.', '357 20th Ave.',
    '424 10th Ave.', '343 18th St.', '448 13th St.', '743 6th St.', '308 13th St.', '929 15th Ave.', '990 19th St.',
    '27 19th St.', '119 12th St.', '156 15th Ave.', '698 3rd St.', '177 24th Ave.', '663 1st St.', '808 5th Ave.',
    '88 10th St.', '776 15th St.', '927 9th St.', '834 7th Ave.', '786 6th Ave.', '598 22nd St.', '653 2nd St.',
    '162 4th St.', '552 4th Ave.', '118 8th St.', '900 3rd St.', '9 14th St.', '921 9th Ave.'
]

test_address_line2s = [
    None, None, 'Apt. R', 'Apt. 786', 'Apt. K', 'Apt. V', None, 'Apt. X', 'Apt. N', None, None, 'Apt. 789',
    'Apt. O', 'Apt. S', 'Apt. J', 'Apt. 778', None, 'Apt. 662', None, 'Apt. P', 'Apt. 717', 'Apt. E', 'Apt. 402',
    'Apt. W', None, 'Apt. 545', None, None, 'Apt. X', None, None, 'Apt. T', 'Apt. 183', None, None, None,
    'Apt. 104', 'Apt. L', 'Apt. 675', 'Apt. C', 'Apt. D', None, 'Apt. V', None, 'Apt. 846', 'Apt. 804', 'Apt. 365',
    'Apt. 447', 'Apt. 330', None, 'Apt. 765', None
]

test_cities = [
    'Example City',
    'Nowhere',
    'Sigil',
    'Pleasantville'
]

test_states = [
    'XY',
    'XX',
    'ZY',
    'ZX'
]

test_zipcodes = [str(n).zfill(5) for n in range(100)]