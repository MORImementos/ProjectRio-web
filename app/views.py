from flask import request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask import current_app as app
import secrets
from . import lm, bc
from .models import db, User, Character, UserCharacterStats, Game, CharacterGameSummary, PitchSummary, ContactSummary, FieldingSummary, ChemistryTable
from .schemas import UserSchema
import json

# Schemas
user_schema = UserSchema()

# === Initalize Character Tables ===
@app.route('/create_character_tables/', methods = ['POST'])
def create_character_tables():
    f = open('./json/MSB_Stats_dec.json')
    character_list = json.load(f)["Characters"]

    for character in character_list:
        chemistry_table = ChemistryTable(
            mario = character['Mario (0x3b)'],
            luigi = character['Luigi (0x3c)'],
            dk = character['DK (0x3d)'],
            diddy = character['Diddy (0x3e)'],
            peach = character['Peach (0x3f)'],
            daisy = character['Daisy (0x40)'],
            yoshi = character['Yoshi (0x41)'],
            baby_mario = character['Baby Mario (0x42)'],
            baby_luigi = character['Baby Luigi (0x43)'],
            bowser = character['Bowser (0x44)'],
            wario = character['Wario (0x45)'],
            waluigi = character['Waluigi (0x46)'],
            koopa_r = character['Koopa(R) (0x47)'],
            toad_r = character['Toad(R) (0x48)'],
            boo = character['Boo (0x49)'],
            toadette = character['Toadette (0x4a)'],
            shy_guy_r = character['Shy Guy(R) (0x4b)'],
            birdo = character['Birdo (0x4c)'],
            monty = character['Monty (0x4d)'],
            bowser_jr = character['Bowser Jr (0x4e)'],
            paratroopa_r = character['Paratroopa(R) (0x4f)'],
            pianta_b = character['Pianta(B) (0x50)'],
            pianta_r = character['Pianta(R) (0x51)'],
            pianta_y = character['Pianta(Y) (0x52)'],
            noki_b = character['Noki(B) (0x53)'],
            noki_r = character['Noki(R) (0x54)'],
            noki_g = character['Noki(G) (0x55)'],
            bro_h = character['Bro(H) (0x56)'],
            toadsworth = character['Toadsworth (0x57)'],
            toad_b = character['Toad(B) (0x58)'],
            toad_y = character['Toad(Y) (0x59)'],
            toad_g = character['Toad(G) (0x5a)'],
            toad_p = character['Toad(P) (0x5b)'],
            magikoopa_b = character['Magikoopa(B) (0x5c)'],
            magikoopa_r = character['Magikoopa(R) (0x5d)'],
            magikoopa_g = character['Magikoopa(G) (0x5e)'],
            magikoopa_y = character['Magikoopa(Y) (0x5f)'],
            king_boo = character['King Boo (0x60)'],
            petey = character['Petey (0x61)'],
            dixie = character['Dixie (0x62)'],
            goomba = character['Goomba (0x63)'],
            paragoomba = character['Paragoomba (0x64)'],
            koopa_g = character['Koopa(G) (0x65)'],
            paratroopa_g = character['Paratroopa(G) (0x66)'],
            shy_guy_b = character['Shy Guy(B) (0x67)'],
            shy_guy_y = character['Shy Guy(Y) (0x68)'],
            shy_guy_g = character['Shy Guy(G) (0x69)'],
            shy_guy_bk = character['Shy Guy(Bk) (0x6a)'],
            dry_bones_gy = character['Dry Bones(Gy) (0x6b)'],
            dry_bones_g = character['Dry Bones(G) (0x6c)'],
            dry_bones_r = character['Dry Bones(R) (0x6d)'],
            dry_bones_b = character['Dry Bones(B) (0x6e)'],
            bro_f = character['Bro(F) (0x6f)'],
            bro_b = character['Bro(B) (0x70)'],
        )

        db.session.add(chemistry_table)
        db.session.commit()

        character = Character(
            char_id = character['Char Id'],
            chemistry_table_id = chemistry_table.id,
            name = character['Char Name'],
            starting_addr = character['Starting Addr'],
            curve_ball_speed = character['Curve Ball Speed (0x0)'],
            fast_ball_speed = character['Fast Ball Speed (0x1)'],
            curve = character['Curve (0x3)'],
            fielding_arm = character['Fielding Arm (righty:0,lefty:1) (0x26)'],
            batting_stance = character['Batting Stance (righty:0,lefty:1) (0x27)'],
            nice_contact_spot_size = character['Nice Contact Spot Size (0x28)'],
            perfect_contact_spot_size = character['Perfect Contact Spot Size (0x29)'],
            slap_hit_power = character['Slap Hit Power (0x2a)'],
            charge_hit_power = character['Charge Hit Power (0x2b)'],
            bunting = character['Bunting (0x2c)'],
            hit_trajectory_mpp = character['Hit trajectory (mid:0,pull:1,push:2) (0x2d)'],
            hit_trajectory_mhl = character['Hit trajectory (mid:0,high:1,low:2) (0x2e)'],
            speed = character['Speed (0x2f)'],
            throwing_arm = character['Throwing Arm (0x30)'],
            character_class = character['Character Class (balance:0,power:1,speed:2,technique:3) (0x31)'],
            weight = character['Weight (0x32)'],
            captain = character['Captain (true:1,false:0) (0x33)'],
            captain_star_hit_or_pitch = character['Captain Star Hit/Pitch (0x34)'],
            non_captain_star_swing = character['Non Captain Star Swing (1:pop fly,2:grounder,3:line drive) (0x35)'],
            non_captain_star_pitch = character['Non Captain Star Pitch (0x36)'],
            batting_stat_bar = character['Batting Stat Bar (0x37)'],
            pitching_stat_bar = character['Pitching Stat Bar (0x38)'],
            running_stat_bar = character['Running Stat Bar (0x39)'],
            fielding_stat_bar = character['Fielding Stat Bar (0x3a)'],
        )

        db.session.add(character)

    db.session.commit()

    return 'Characters added...'



# == User Routes ==
# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout/')
def logout():
    logout_user()
    
    resp = jsonify(success=True)
    return resp

@app.route('/register/', methods=['POST'])
def register():    
    in_username = request.json['Username']
    in_password = request.json['Password']
    in_email    = request.json['Email']

    # filter User out of database through username
    user = User.query.filter_by(username=in_username).first()

    # filter User out of database through email
    user_by_email = User.query.filter_by(email=in_email).first()

    if user or user_by_email:
        return abort(409, description='Username has already been taken')
    elif in_username.isalnum() == False:
        return abort(406, description='Provided username is not alphanumeric')
    else:
        new_user = User(in_username, in_email, in_password)
        db.session.add(new_user)
        db.session.commit()

        # === Create UserCharacterStats tables ===
        characters = Character.query.all()
        for character in characters:
            user_character_stats = UserCharacterStats(new_user.id, character.char_id)
            db.session.add(user_character_stats)
            db.session.commit()

    return user_schema.dump(new_user)

# Authenticate user, login via username or email
@app.route('/login/', methods=['POST'])
def login():
    in_username = request.json['Username']
    in_password = request.json['Password']
    in_email    = request.json['Email']

    # filter User out of database through username
    user = User.query.filter_by(username=in_username).first()

    # filter User out of database through email
    user_by_email = User.query.filter_by(email=in_email).first()

    if user or user_by_email:
        user_to_login = user if user else user_by_email
        if bc.check_password_hash(user_to_login.password, in_password):
            login_user(user_to_login)
            return user_schema.dump(user_to_login)
        else:
            return abort(401, description='Incorrect password')
    else:
        return abort(406, description='User does not exist')

#GET will retreive user key, POST with empty JSON will generate new rio key and return it
@app.route('/key/', methods=['GET', 'POST'])
@login_required
def update_rio_key():
    if current_user.is_authenticated:
        # Return Key
        if request.method == 'GET':
            return user_schema.dump(current_user)
        # Generate new key and return it
        elif request.method == 'POST':
            current_user.rio_key  = secrets.token_urlsafe(32)            
            db.session.commit()
            return user_schema.dump(current_user)



# === Upload Game Data ===
@app.route('/upload_game_data/', methods = ['POST'])
def populate_db():
    #get players from db User table
    home_player = User.query.filter_by(username=request.json['Home Player']).first()
    away_player = User.query.filter_by(username=request.json['Away Player']).first()

    game = Game(
        game_id = request.json['GameID'],
        away_player_id = away_player.id,
        home_player_id = home_player.id,
        date_time = request.json['Date'],
        ranked = request.json['Ranked'],
        stadium_id = request.json['StadiumID'],
        away_score = request.json['Away Score'],
        home_score = request.json['Home Score'],
        innings_selected = request.json['Innings Selected'],
        innings_played = request.json['Innings Played'],
        quitter = request.json['Quitter Team'],
    )

    db.session.add(game)
    db.session.commit()

    # === Character Game Summary ===
    player_stats = request.json['Player Stats']
    teams = {
        'Home': [None] * 9,
        'Away': [None] * 9,
    }
    for character in player_stats:
        defensive_stats = character['Defensive Stats']
        offensive_stats = character['Offensive Stats']

        character_game_summary = CharacterGameSummary(
            game_id = game.game_id,
            team_id = 0 if character['Team'] == 'Home' else 1,
            char_id = Character.query.filter_by(name=character["Character"]).first().char_id,
            roster_loc = character['RosterID'],
            superstar = True if character['Is Starred'] == 1 else False,
            batters_faced = defensive_stats['Batters Faced'],
            runs_allowed = defensive_stats['Runs Allowed'],
            batters_walked = defensive_stats['Batters Walked'],
            batters_hit = defensive_stats['Batters Hit'],
            hits_allowed = defensive_stats['Hits Allowed'],
            homeruns_allowed = defensive_stats['HRs Allowed'],
            pitches_thrown = defensive_stats['Pitches Thrown'],
            stamina = defensive_stats['Stamina'],
            was_pitcher = defensive_stats['Was Pitcher'],
            batter_outs = defensive_stats['Batter Outs'],
            strikeouts_pitched = defensive_stats['Strikeouts'],
            star_pitches_thrown = defensive_stats['Star Pitches Thrown'],
            big_plays = defensive_stats['Big Plays'],
            innings_pitched = defensive_stats['Innings Pitched'],
            at_bats = offensive_stats['At Bats'],
            hits = offensive_stats['Hits'],
            singles = offensive_stats['Singles'],
            doubles = offensive_stats['Doubles'],
            triples = offensive_stats['Triples'],
            homeruns = offensive_stats['Homeruns'],
            strikeouts = offensive_stats['Strikeouts'],
            walks_bb = offensive_stats['Walks (4 Balls)'],
            walks_hit = offensive_stats['Walks (Hit)'],
            rbi = offensive_stats['RBI'],
            bases_stolen = offensive_stats['Bases Stolen'],
            star_hits = offensive_stats['Star Hits'],
        )

        db.session.add(character_game_summary)
        db.session.commit()

        teams[character['Team']][character['RosterID']] = character_game_summary
        
    for character in player_stats:

        # Update CharacterUserStats
        if character['Team'] == 'Home':
            user_char_stats = home_player.user_character_stats.filter_by(char_id=Character.query.filter_by(name=character["Character"]).first().char_id).first()
            character_game_summary = teams['Home'][character['RosterID']]
        else: 
            user_char_stats = away_player.user_character_stats.filter_by(char_id=Character.query.filter_by(name=character["Character"]).first().char_id).first()
            character_game_summary = teams['Away'][character['RosterID']]

        user_char_stats.num_of_games += 1
        user_char_stats.at_bats += character_game_summary.at_bats
        user_char_stats.hits += character_game_summary.hits
        user_char_stats.walks_bb += character_game_summary.walks_bb
        user_char_stats.walks_hit += character_game_summary.walks_hit
        user_char_stats.bases_stolen += character_game_summary.bases_stolen
        user_char_stats.strikeouts += character_game_summary.strikeouts
        user_char_stats.innings_pitched += character_game_summary.innings_pitched
        user_char_stats.batters_faced += character_game_summary.batters_faced
        user_char_stats.runs_allowed += character_game_summary.runs_allowed
        user_char_stats.defensive_star_pitches += character_game_summary.star_pitches_thrown       


        for pitch in character['Pitch Summary']:
            pitch_summary = PitchSummary(
                batter_id = teams[character['Team']][character['RosterID']].id,
                pitcher_id = teams['Home' if character['Team'] == 'Away' else 'Away'][pitch["Pitcher Roster Location"]].id,
                inning = pitch['Inning'],
                half_inning = pitch['Half Inning'],
                batter_score = pitch['Batter Score'],
                pitcher_score = pitch['Fielder Score'],
                balls = pitch['Balls'],
                strikes = pitch['Strikes'],
                outs = pitch['Outs'],
                runner_on_1 = True if pitch['Runners on Base'][2] == 1 else False,
                runner_on_2 = True if pitch['Runners on Base'][1] == 1 else False,
                runner_on_3 = True if pitch['Runners on Base'][0] == 1 else False,
                chem_links_ob = pitch['Chemistry Links on Base'],
                star_chance = pitch['Star Chance'],
                batter_stars = pitch['Batter Stars'],
                pitcher_stars = pitch['Pitcher Stars'],
                pitcher_handedness = pitch['Pitcher Handedness'],
                pitch_type = pitch['Pitch Type'],
                charge_pitch_type = pitch['Charge Pitch Type'],
                star_pitch = pitch['Star Pitch'],
                pitch_speed = pitch['Pitch Speed'],
                type_of_swing = pitch['Type of Swing'],
                rbi = pitch['RBI'],
                num_outs = pitch['Number Outs During Play'],
                result_inferred = pitch['Final Result - Inferred'],
                result_game = pitch['Final Result - Game'],
            )

            db.session.add(pitch_summary)
            db.session.commit()

            # === Contact Summary === 
            if pitch['Contact Summary']:
                contact_summary = ContactSummary(
                    pitchsummary_id = pitch_summary.id,
                    type_of_contact = pitch['Contact Summary'][0]['Type of Contact'],
                    charge_power_up = pitch['Contact Summary'][0]['Charge Power Up'],
                    charge_power_down = pitch['Contact Summary'][0]['Charge Power Down'],
                    star_swing_five_star = pitch['Contact Summary'][0]['Star Swing Five-Star'],
                    input_direction = pitch['Contact Summary'][0]['Input Direction'],
                    batter_handedness = pitch['Batter Handedness'],
                    ball_angle = pitch['Contact Summary'][0]['Ball Angle'],
                    ball_horiz_power = pitch['Contact Summary'][0]['Ball Horizontal Power'],
                    ball_vert_power = pitch['Contact Summary'][0]['Ball Vertical Power'],
                    ball_x_velocity = pitch['Contact Summary'][0]['Ball Velocity - X'],
                    ball_y_velocity = pitch['Contact Summary'][0]['Ball Velocity - Y'],
                    ball_z_velocity = pitch['Contact Summary'][0]['Ball Velocity - Z'],
                    ball_x_pos = pitch['Contact Summary'][0]['Ball Acceleration - X'],
                    ball_y_pos = pitch['Contact Summary'][0]['Ball Acceleration - Y'],
                    ball_z_pos = pitch['Contact Summary'][0]['Ball Acceleration - Z'],
                    ball_x_pos_upon_hit = pitch['Contact Summary'][0]['Ball Position Upon Contact- x'],
                    ball_y_pos_upon_hit = pitch['Contact Summary'][0]['Ball Position Upon Contact- Y'],
                )

                db.session.add(contact_summary)
                db.session.commit()

                # === Fielding Summary ===
                if pitch['Contact Summary'][0]['Fielding Summary']:
                    fielder_roster_location = pitch['Contact Summary'][0]['Fielding Summary'][0]['Fielder Roster Location']
                    fielder_team = 'Home' if character['Team'] == 'Away' else 'Away'

                    fielding_summary = FieldingSummary(
                        contact_summary_id = contact_summary.id,
                        fielder_character_game_summary_id = teams[fielder_team][fielder_roster_location].id,
                        position = pitch['Contact Summary'][0]['Fielding Summary'][0]['Fielder Position'],
                    )

                db.session.add(fielding_summary)
                db.session.commit()

        db.session.add(user_char_stats)
        db.session.commit()

    return 'Successfully added...'



# === Get Characters ===
@app.route('/characters/', methods = ['GET'])
def get_characters():
    characters = []
    for character in Character.query.all():
        characters.append(character.to_dict())

    return {
        'characters': characters
        }

@app.route('/user_characters/<user>', methods = ['GET'])
def get_user_character_stats(user):
    characters = []
    user_characters = User.query.filter_by(username=user).first().user_character_stats.all()
    
    for character in user_characters:
        characters.append(character.to_dict())
    
    return {
        'User Characters': characters
        }
