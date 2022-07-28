from keep_alive import keep_alive
import discord, sqlite3, os
from timer import User_timer

client = discord.Client()
con = sqlite3.connect('db.db')
cursor = con.cursor()

Timers = {}
in_battle = 0
deck = ['deck', '迪克', '甲板']
austin = ['austin', 'Austin', '奥斯汀', '奥斯咕', '奥斯丁']

bug = ['源石虫', 5, 1, 0, 5]
dog = ['猎狗', 15, 2, 1, 10]
dummy = ['测试用假人', 10000, 0, 0, 0]
soldier = ['士兵', 30, 10, 0, 15]
ausking = ['奥神', 99999, 5000, 5000, 100000, 0]
archer = ['弩手', 50, 15, 1, 20]
airborne = ['空降兵', 70, 20, 2, 25]
sword = ['剑士', 100, 20, 5, 30]
shield = ['轻甲卫兵', 110, 25, 5, 35]
junkman = ['拾荒者', 200, 35, 10, 40]
mobs = {'bug':bug,'dog':dog,'dummy':dummy,'soldier':soldier,'ausking':ausking,'archer':archer,'airborne':airborne,'sword':sword,'shield':shield,'junkman':junkman}
shop = {'sword':50, 'AK47':500, 'shield':50, 'apple':20, 'pot':5}

"""con.execute('''CREATE TABLE DB
 (ID INT PRIMARY KEY,
  NAME           TEXT,
  LOC            INT,
  GOLD           INT,
  LVL            INT,
  HP_MAX         INT,
  MP_MAX         INT,
  HP             INT,
  MP             INT,
  ATK            INT,
  DEF            INT);''')"""

#con.execute("INSERT INTO DB VALUES(1145141919810, 'austin', 0, 0, 1, 20, 20, 20, 20, 1, 0)")
#con.commit()

#con.execute(f"DELETE from DB where ID = 804197632285081620")
#con.commit()

#con.execute(f"UPDATE DB SET NAME = 'xgt' where ID = 687479429496307929")
#con.commit()

#con.execute("ALTER TABLE DB ADD COLUMN IN_BATTLE INT")

for info in con.execute("SELECT * from DB"):
  print(f'ID:{info[0]} name:{info[1]} location:{info[2]} gold:{info[3]} level:{info[4]} max_hp:{info[5]} max_mp:{info[6]} hp:{info[7]} mp:{info[8]} atk:{info[9]} def:{info[10]}\n')
  
def unique(ID):
  for id in con.execute("SELECT ID FROM DB"):
    if id[0] == ID:
      return False
  return True

@client.event
async def on_ready():
  Timers["deck"] = User_timer(300)
  Timers["austin"] = User_timer(300)
  Timers["42"] = User_timer(300)
  Timers["maze"] = User_timer(300)
  Timers["fox"] = User_timer(300)

@client.event
async def on_message(message):
  global in_battle
  msg = message.content
  au = message.author

  if au == client.user:
    return

  #804197632285081620

  if msg.startswith('$'):
    if unique(au.id) and not msg[1:].startswith('reg'):
      await message.channel.send('Use "$reg name" to register')
      return
    
    if msg[1:].startswith('reg '):
      if unique(au.id):
        if 1 <= len(msg[5:]):
          await message.channel.send(f'Welcome {msg[5:]}')
          val = (au.id, msg[5:], 0, 0, 1, 20, 20, 20, 20, 1, 0)
          con.execute("INSERT INTO DB VALUES(?,?,?,?,?,?,?,?,?,?,?)", val)
          con.commit()
        else:
          await message.channel.send('at least one character')
      else:
        await message.channel.send('Accound already exist')

    elif msg[1:] == 'richladyhugme':
      con.execute(f'UPDATE DB SET GOLD = GOLD+100 where ID = {au.id}')
      con.commit
      await message.channel.send('富婆抱抱我！(金币+100)||(节操-1)||')

    elif msg[1:] == 'whosyourdaddy':
      con.execute(f'UPDATE DB SET ATK = ATK+1000 where ID = {au.id}')
      con.execute(f'UPDATE DB SET DEF = DEF+1000 where ID = {au.id}')
      con.commit
      
    elif msg[1:] == 'stat':
      cursor.execute(f'SELECT * FROM DB WHERE ID = {au.id}')
      info = cursor.fetchall()[0]
      await message.channel.send(f'Name: {info[1]}\nGold: {info[3]}\nLevel: {info[4]}\nHP: {info[7]}/{info[5]}\nMP: {info[8]}/{info[6]}\nATK: {info[9]}\nDEF: {info[10]}')

    elif msg[1:] == 'list':
      list = "{0:<10}{1:<6}{2:<5}{3:<5}{4:<5}".format("Name","Level","HP","ATK","DEF")
      for info in con.execute("SELECT NAME, LVL, HP, ATK, DEF from DB ORDER BY LVL DESC"):
        list = list + "\n{0:<10}{1:<6}{2:<5}{3:<5}{4:<5}".format(info[0],info[1],info[2],info[3],info[4])
      await message.channel.send(f'```{list}```')

    elif msg[1:] == 'del':
      if unique(au.id):
        await message.channel.send('Account does not exist')
      else:
        con.execute(f"DELETE from DB where ID = {au.id}")
        con.commit()
        await message.channel.send('Account deleted')

    elif msg[1:].startswith('info ') or msg[1:] == 'info':
      if msg[6:] in mobs:
        target = mobs[msg[6:]]
        await message.channel.send(file=discord.File(f'mobs/{msg[6:]}.png'))
        await message.channel.send(f'Name: {target[0]}\nHP: {target[1]}\nATK: {target[2]}\nDEF: {target[3]}\nGold: {target[4]}')
      else:
        list = ""
        for mob in mobs:
          list = list + mob + "\n"
        await message.channel.send(list)

    elif msg[1:] == 'help':
      await message.channel.send('Help: $help\nRegister: $reg name\nStatistics: $stat\nList all: $list\nTarget : $info target\nAttack: $atk target\nShop: $shop item\nDelete account: $del')

    elif msg[1:].startswith('shop ') or msg[1:] == 'shop':
      if msg[6:] in shop:
        cursor.execute(f'SELECT GOLD, HP_MAX, HP from DB WHERE ID = {au.id}')
        u = cursor.fetchall()[0]
        if u[0] >= shop[msg[6:]]:
          con.execute(f'UPDATE DB SET GOLD = GOLD-{shop[msg[6:]]} where ID = {au.id}')
          if msg[6:] == "sword":
            con.execute(f'UPDATE DB SET ATK = ATK+1 where ID = {au.id}')
            await message.channel.send('攻击更加凌厉了！')
          if msg[6:] == "AK47":
            con.execute(f'UPDATE DB SET ATK = ATK+10 where ID = {au.id}')
            await message.channel.send('大人，时代变了！')
          elif msg[6:] == "shield":
            con.execute(f'UPDATE DB SET DEF = DEF+1 where ID = {au.id}')
            await message.channel.send('防御力提高了！')
          elif msg[6:] == "apple":
            con.execute(f'UPDATE DB SET HP_MAX = HP_MAX+5 where ID = {au.id}')
            await message.channel.send('生命上限提高了！')
          elif msg[6:] == "pot":
            con.execute(f'UPDATE DB SET HP = {min(u[1], u[2]+10)} where ID = {au.id}')
            await message.channel.send('生命恢复了！')
          con.commit()
        else:
          await message.channel.send('Not enough gold')
      else:
        list = ""
        for item in shop:
          list = list+item+": "+str(shop[item])+"\n"
        await message.channel.send(list)
    
    elif msg[1:].startswith('atk '):
      target = {}
      if in_battle == 1:
        await message.channel.send('battle in progress')
        return
      elif msg[5:] in mobs:
        target = mobs[msg[5:]]
      else:
        await message.channel.send('Unknown target')
        return
      cursor.execute(f'SELECT HP, ATK, DEF from DB WHERE ID = {au.id}')
      u = cursor.fetchall()[0]
      if u[1] <= target[3] or u[0] == 0:
        await message.channel.send('打不过 溜了')
        return
      uhp = u[0]
      thp = target[1]
      in_battle = 1
      record = ""
      await message.channel.send(f'一只野生的{target[0]}出现了！',file=discord.File(f'mobs/{msg[5:]}.png'))
      while thp > 0 and uhp > 0:
        uhp -= max(target[2]-u[2], 0)
        thp -= max(u[1]-target[3], 0)
        uhp = max(uhp, 0)
        thp = max(thp, 0)
        if len(record) > 1900:
          await message.channel.send(record)
          record = ""
        record = record+"你攻击了"+target[0]+"造成了"+str(max(u[1]-target[3], 0))+"点伤害！你当前生命:"+str(uhp)+"\n"+target[0]+"攻击了你造成了"+str(max(target[2]-u[2], 0))+"点伤害！"+target[0]+"当前生命:"+str(thp)+"\n"
      if thp <= 0:
        await message.channel.send(f'{record}{target[0]}寄了！战斗胜利☆☆☆获得金币{target[4]}！当前生命:{uhp}')
      else:
        await message.channel.send(f'{record}行动失败！丢人，你给我退出战场！')
      con.execute(f'UPDATE DB SET HP = {uhp} where ID = {au.id}')
      con.execute(f'UPDATE DB SET GOLD = GOLD+{target[4]} where ID = {au.id}')
      con.commit()
      in_battle = 0
    
    else:
      await message.channel.send('Unknown command. Type "$help" for help')

  if client.user.mention in msg:
    await message.channel.send('SB?')

  if any(word in msg for word in austin) or au.id == 687479429496307929:
    if Timers["austin"].check_cooldown():
      Timers["austin"].cooldown()
      await message.channel.send('咕咕咕')

  if any(word in msg for word in deck) or au.id == 861154258082201621:
    if (Timers["deck"].check_cooldown()):
      Timers["deck"].cooldown()
      await message.channel.send('dklp')

  if au.id == 614967277833551895:
    if Timers["42"].check_cooldown():
      Timers["42"].cooldown()
      await message.channel.send('42')

  if au.id == 711802374989283329:
    await message.add_reaction('<nojt:987618578608058388>')

  if "🦇" in msg:
    await message.channel.send(':bat::no_entry_sign:')

  if au.id == 375251797679538177:
    await message.add_reaction('🐑')

  if au.id == 764356009711501333:
    if (Timers["fox"].check_cooldown()):
      Timers["fox"].cooldown()
      await message.channel.send('<:qwq:987521867340472391>')

  if au.id == 244331186447581186:
    if (Timers["maze"].check_cooldown()):
      Timers["maze"].cooldown()
      await message.channel.send(file=discord.File("maze.gif"))

keep_alive()
client.run(os.environ['TOKEN'])