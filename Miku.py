import discord
import asyncio
import random
# import urllib.parse
# import urllib
import youtube_dl
import openpyxl
import datetime
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord.ext import commands


token = "bot_token"

client = commands.Bot(command_prefix='!')
# intents = discord.Intents.default()
# client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("봇 준비 완료!")
    print(client.user.name)
    print("---------------")
    game = discord.Game("!명령어 라고 쳐주세요")
    await client.change_presence(status=discord.Status.online, activity=game)




@client.command()
async def 미쿠(ctx):
    await ctx.send("初音ミク 登場!")

@client.command()
async def 명령어(ctx):
    embed = discord.Embed(title="명령어", color=0x62c1cc)
    embed.set_thumbnail(url="https://i.imgur.com/094U5yG.jpg")
    embed.add_field(name="!미쿠",value="`하츠네 미쿠 등장!`")
    embed.add_field(name="!따라해",value="`따라하기`",inline=False)
    embed.add_field(name="!입장",value="`음성 채팅 입장`")
    embed.add_field(name="!재생",value="`노래 재생 (재생 뒤 youtube url)`")
    embed.add_field(name="!퇴장",value="`음성 채팅 퇴장`",inline=False)
    embed.add_field(name="!경고",value="`경고주기`")
    embed.add_field(name="!경고보기",value="`경고보기`")
    embed.add_field(name="!경고초기화",value="`경고초기화`",inline=False)
    embed.add_field(name="!기능추가",value="`기능추가`")
    embed.add_field(name="!기능보기",value="`기능보기`")
    embed.add_field(name="!기능삭제",value="`기능삭제`")
    embed.add_field(name="!기능초기화",value="`기능초기화`",inline=False)
    embed.add_field(name="!타이머",value="`타이머(초)`",inline=False)
    embed.add_field(name="!알람추가",value="`알람추가`")
    embed.add_field(name="!알람보기",value="`알람보기`")
    embed.add_field(name="!알람삭제",value="`알람삭제`")
    embed.add_field(name="!알람초기화",value="`알람초기화`")
    embed.add_field(name="!투표",value="`ex)!투표 투표제목/(투표1)/(투표2)`")
    embed.add_field(name="!신음",value="`미쿠의 신음소리`",inline=False)
    embed.add_field(name="!메세지삭제",value="`메세지 삭제 (개수)`",inline=False)
    embed.add_field(name="!사진목록1",value="`목록 1`")
    embed.add_field(name="!사진목록2",value="`목록 2`")
    embed.add_field(name="!사진",value="`사진(숫자)`")

    await ctx.send(embed=embed)

@client.command()
async def 따라해(ctx):
    msg = ctx.message.content[5:]
    await ctx.send(msg)

@client.command()
async def 입장(ctx):
    await ctx.message.author.voice.channel.connect()
    await ctx.message.channel.send("보이스채널 입장합니다.")
    
@client.command()
async def 퇴장(ctx):
    global voice
    for vc in client.voice_clients:
        if vc.guild == ctx.message.guild:
            voice = vc
        
    await voice.disconnect()
    await ctx.message.channel.send("보이스채널 퇴장합니다.")

@client.command()
async def 재생(ctx):
    global voice
    for vc in client.voice_clients:
        if vc.guild == ctx.message.guild:
            voice = vc

    url = ctx.message.content.split(" ")[1]
    option = {
        # 'outtmpl' : "file/" + url.split('=')[1] + ".mp3"
        'outtmpl' : "file/" + url.split('=')[1] + ".mp3",
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(option) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        title = info["title"]

    voice.play(discord.FFmpegPCMAudio("file/" + url.split('=')[1] + ".mp3"))
    await ctx.message.channel.send(title + "을 재생합니다.")

@client.command()
async def 경고(ctx):
    msg = ctx.message.content[4:]
    file = openpyxl.load_workbook("경고.xlsx")
    sheet = file.active
    i = 1
    while True:
        if sheet["A" + str(i)].value == str(msg):
            sheet["B" + str(i)].value = int(sheet["B" + str(i)].value) + 1
            file.save("경고.xlsx")
            await ctx.message.channel.send("경고를 1회 받았습니다.")
            if sheet["B" + str(i)].value == 2:
                await ctx.message.channel.send("누적 2회")
            elif sheet["B" + str(i)].value == 3:
                await ctx.message.channel.send("누적 3회")
            elif sheet["B" + str(i)].value == 4:
                await ctx.message.channel.send("누적 4회")
            elif sheet["B" + str(i)].value == 5:
                await ctx.message.channel.send("누적 5회")
            elif sheet["B" + str(i)].value == 6:
                await ctx.message.channel.send("누적 6회")
            elif sheet["B" + str(i)].value == 7:
                await ctx.message.channel.send("누적 7회")
            elif sheet["B" + str(i)].value == 8:
                await ctx.message.channel.send("누적 8회")
            elif sheet["B" + str(i)].value == 9:
                await ctx.message.channel.send("누적 9회")
            elif sheet["B" + str(i)].value == 10:
                await ctx.message.channel.send("누적 10회 퇴장조치")
            break
        if sheet["A" + str(i)].value == None:
            sheet["A" + str(i)].value = str(msg)
            sheet["B" + str(i)].value = 1
            file.save("경고.xlsx")
            await ctx.message.channel.send("경고를 1회 받았습니다.")
            await ctx.message.channel.send("누적 1회")
            break
        i+=1

@client.command()
async def 경고보기(ctx):
    file = openpyxl.load_workbook("경고.xlsx")
    sheet = file.active
    i=1
    try:
        for i in range(1,100):
            await ctx.message.channel.send(sheet.cell(i,1).value)
            await ctx.message.channel.send(sheet.cell(i,2).value)
            i+=1
    except :
        await ctx.message.channel.send("--------")
        await ctx.message.channel.send("여기까지")

@client.command()
async def 경고초기화(ctx):
    file = openpyxl.load_workbook("경고.xlsx")
    sheet  = file.active
    sheet.delete_cols(1)
    sheet.delete_cols(1)
    file.save("경고.xlsx")
    await ctx.message.channel.send("경고가 초기화 되었습니다.")



@client.command()
async def 기능추가(ctx):
    msg = ctx.message.content[6:]
    file = openpyxl.load_workbook("기능추가.xlsx")
    sheet  = file.active
    i=1
    while True:
        if sheet["A" + str(i)].value == None:
            sheet["A" + str(i)].value = str(msg)
            file.save("기능추가.xlsx")
            await ctx.message.channel.send(msg + " 기능이 추가 되었습니다.")
            break
        i+=1

@client.command()
async def 기능보기(ctx):
    file = openpyxl.load_workbook("기능추가.xlsx")
    sheet = file.active
    i=1
    try:
        for i in range(1,100):
            await ctx.message.channel.send(sheet.cell(i,1).value)
            i+=1
    except :
        await ctx.message.channel.send("--------")
        await ctx.message.channel.send("여기까지")

@client.command()
async def 기능삭제(ctx):
    msg = ctx.message.content[6:]
    file = openpyxl.load_workbook("기능추가.xlsx")
    sheet  = file.active
    i=1
    while True:
        if sheet["A" + str(i)].value == str(msg):
            sheet.delete_rows(i)
            file.save("기능추가.xlsx")
            await ctx.message.channel.send(msg + " 기능이 삭제 되었습니다.")
            break
        i+=1

@client.command()
async def 기능초기화(ctx):
    file = openpyxl.load_workbook("기능추가.xlsx")
    sheet  = file.active
    sheet.delete_cols(1)
    file.save("기능추가.xlsx")
    await ctx.message.channel.send("기능이 초기화 되었습니다.")

@client.command()
async def 타이머(ctx):
    msg = ctx.message.content[5:]
    sec = int(msg)

    for i in range(sec, 0, -1):
        time.sleep(1)
        await ctx.message.channel.send(embed=discord.Embed(description= str(i) + "초"))
    else:
        await ctx.message.channel.send(embed=discord.Embed(description='타이머 종료'))

@client.command()
async def 알람추가(ctx):
    msg = ctx.message.content[6:]
    file = openpyxl.load_workbook("알람.xlsx")
    sheet  = file.active
    i=1
    while True:
        if sheet["A" + str(i)].value == None:
            li = msg.split(" ")
            da1 = li.pop(0)
            da2 = li.pop(0)
            da3 = li.pop(0)
            da4 = li.pop(0)
            da5 = li.pop(0)
            dd = da1 + da2 + da3 + da4 +da5 
            sheet["A" + str(i)].value = str(dd)
            file.save("알람.xlsx")
            year = dd[:4]
            month = dd[4:6]
            day = dd[6:8]
            hour = dd[8:10]
            minu = dd[10:]
            await ctx.message.channel.send(year + "년 " + month + '월 ' + day + "일 " + hour + '시 ' + minu + "분 알람이 추가되었습니다.")
            break
        i+=1

@client.command()
async def 알람삭제(ctx):
    msg = ctx.message.content[6:]
    file = openpyxl.load_workbook("알람.xlsx")
    sheet  = file.active
    i=1
    while True:
        li = msg.split(" ")
        da1 = li.pop(0)
        da2 = li.pop(0)
        da3 = li.pop(0)
        da4 = li.pop(0)
        da5 = li.pop(0)
        dd = da1 + da2 + da3 + da4 +da5 
        if sheet["A" + str(i)].value == str(dd):
            sheet.delete_rows(i)
            file.save("알람.xlsx")
            year = dd[:4]
            month = dd[4:6]
            day = dd[6:8]
            hour = dd[8:10]
            minu = dd[10:]
            await ctx.message.channel.send(year + "년 " + month + '월 ' + day + "일 " + hour + '시 ' + minu + "분 알람이 삭제 되었습니다.")
            break
        i+=1

@client.command()
async def 알람보기(ctx):
    file = openpyxl.load_workbook("알람.xlsx")
    sheet  = file.active
    i=1
    try:
        for i in range(1,100):
            dd = sheet.cell(i,1).value
            year = dd[:4]
            month = dd[4:6]
            day = dd[6:8]
            hour = dd[8:10]
            minu = dd[10:]
            await ctx.message.channel.send(year + "년 " + month + '월 ' + day + "일 " + hour + '시 ' + minu + "분")
            i+=1
    except :
        await ctx.message.channel.send("--------")
        await ctx.message.channel.send("여기까지")

@client.command()
async def 알람초기화(ctx):
    file = openpyxl.load_workbook("알람.xlsx")
    sheet  = file.active
    sheet.delete_cols(1)
    file.save("알람.xlsx")
    await ctx.message.channel.send("알람이 초기화 되었습니다.")
    
# @client.event
# async def online():
#     file = openpyxl.load_workbook("알람.xlsx")
#     sheet  = file.active
#     i = 1
#     while True:
#         dt = datetime.datetime.now()
#         dt = dt.strftime('%Y/%m/%d %H:%M')

#         li = dt 
#         li1 = li.split(" ")

#         day = li1.pop(0)
#         time = li1.pop(0)

#         day = day.split("/")
#         time = time.split(":")

#         day1 = day.pop(0)
#         time1 = time.pop(0)

#         day2 = day.pop(0)
#         time2 = time.pop(0)

#         day3 = day.pop(0)

#         last = day1 + day2 + day3 + time1 + time2
        
#         print(last)

#         if sheet["A" + str(i)].value == last:
#             sheet.delete_rows(i)
#             file.save("알람.xlsx")
#             await ctx.message.channel.send("@averyone")
#             break
#         i+=1

@client.command()
async def 신음(ctx):
    await ctx.send("하아.. 하앙..")
    time.sleep(1)
    await ctx.send("흐읏..!!")
    time.sleep(2)
    await ctx.send("읏..!! 하앙..")
    time.sleep(1)
    await ctx.send("주인님.. 하읏.. 안되요")
    time.sleep(2)
    await ctx.send("흐읏!!!! 하.. 다리의 힘이 풀려..")
    time.sleep(1)
    await ctx.send("하앙!!! 아항ㅇ!!")
    time.sleep(3)
    await ctx.send("주인님 더.. 더.. 쎄게")
    time.sleep(1)
    await ctx.send("아흥!!!항..")
    time.sleep(2)
    await ctx.send("간닷!!흥ㅅ..ㄱ..가버렷!!")
    time.sleep(1)
    await ctx.send("헤으응.. 하응.. 좋아요 주인님")
    time.sleep(3)
    await ctx.send("(꿀꺽..) 하.. 맛있어요..")
    time.sleep(1)
    await ctx.send("사랑해요.. 주인님..")

@client.command()
async def 메세지삭제(ctx):
    number = int(ctx.message.content.split()[1])
    await ctx.message.channel.purge(limit=number + 1)
    await ctx.message.channel.send(f"{number}개 메세지 삭제완료")

@client.command()
async def 투표(ctx):
    vote = ctx.message.content[4:].split("/")
    await ctx.message.channel.send("★투표 - " + vote[0])
    for i in range(1, len(vote)):
        choose = await ctx.message.channel.send("```" + vote[i] + "```")
        await choose.add_reaction('👍')

# @client.command()
# async def 공건불러(ctx):
    # for i in range(1,50):
        # msg = "<@{}>".format(str(354168092643033090))
        # time.sleep(1)
        # await ctx.message.channel.send(msg)

# @client.command()
# async def 주기알람(ctx):
#     msg = ctx.message.content[6:]
#     await ctx.message.channel.send(msg + "일 마다 알람이 울립니다.")
#     await ctx.message.channel.send("*단 프로그램이 켜져있어야 합니다. (또는 호스팅)*")
#     msg = int(msg)
#     while True:
#         time.sleep(86400*msg)
#         await ctx.message.channel.send("주기 알람 @everyone")

@client.command()
async def 주기알람(ctx):
    msg = ctx.message.content[6:]
    await ctx.message.channel.send(msg + "시간 마다 알람이 울립니다.")
    await ctx.message.channel.send("*단 프로그램이 켜져있어야 합니다. (또는 호스팅)*")
    msg = int(msg)
    while True:
        time.sleep(3600*msg)
        await ctx.message.channel.send("주기 알람")

@client.command()
async def 사진목록1(ctx):
    embed = discord.Embed(title="사진", color=0x62c1cc)
    embed.add_field(name="1", value="최초미쿠")
    embed.add_field(name="2", value="보컬미쿠")
    embed.add_field(name="3", value="사쿠라미쿠")
    embed.add_field(name="4", value="하츄네미쿠")
    embed.add_field(name="5", value="자츠네미쿠")
    embed.add_field(name="6", value="하츠네즈미")
    embed.add_field(name="7", value="야미네아쿠")
    embed.add_field(name="8", value="노로네키쿠")
    embed.add_field(name="9", value="카루네시에")
    embed.add_field(name="10", value="유키미쿠")
    embed.add_field(name="11", value="레이싱미쿠")
    embed.add_field(name="12", value="보틀미쿠")
    embed.add_field(name="13", value="아니마사식미쿠")
    embed.add_field(name="14", value="Lat식미쿠")
    embed.add_field(name="15", value="나노하1052식미쿠")
    embed.add_field(name="16", value="러브식미쿠")
    embed.add_field(name="17", value="온다식미쿠")
    embed.add_field(name="18", value="어피어런스미쿠")
    embed.add_field(name="19", value="xs식미쿠")
    embed.add_field(name="20", value="Tda식미쿠")
    await ctx.send(embed=embed)
@client.command()
async def 사진목록2(ctx):
    embed = discord.Embed(title="사진", color=0x62c1cc)
    embed.add_field(name="21", value="REMmaple식V3미쿠")
    embed.add_field(name="22", value="키오식미쿠")
    embed.add_field(name="23", value="디바풍미쿠")
    embed.add_field(name="24", value="아피미쿠")
    embed.add_field(name="25", value="Ula식미쿠")
    embed.add_field(name="26", value="마레욘식미쿠")
    embed.add_field(name="27", value="YYB식미쿠")
    embed.add_field(name="28", value="Gency식미쿠")
    embed.add_field(name="29", value="시온식미쿠")
    embed.add_field(name="30", value="하츠키식미쿠")
    embed.add_field(name="31", value="별이빛나는미쿠")
    embed.add_field(name="32", value="피쿠치식미쿠")
    embed.add_field(name="33", value="유키하네식미쿠")
    embed.add_field(name="34", value="코론식미쿠")
    embed.add_field(name="35", value="로쿠고식미쿠")
    embed.add_field(name="36", value="Digitrevx식미쿠")
    embed.add_field(name="37", value="미야식미쿠")
    embed.add_field(name="38", value="넨드로이드미쿠")
    embed.add_field(name="39", value="고양이미쿠")
    embed.add_field(name="40", value="비키니미쿠")
    await ctx.send(embed=embed)

@client.command()
async def 사진(ctx):
    embed = discord.Embed(imestamp=ctx.message.created_at,color=0x62c1cc)
    msg = ctx.message.content[4:]
    msg = int(msg)
    if msg == 1:
        embed.set_image(url="https://i.imgur.com/JG7JXpA.jpg")
        
        await ctx.message.channel.send(embed=embed)
    elif msg == 2:
        embed.set_image(url="https://i.imgur.com/tWvu4xk.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 3:
        embed.set_image(url="https://i.imgur.com/lmTycvB.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 4:
        embed.set_image(url="https://i.imgur.com/khoYN5r.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 5:
        embed.set_image(url="https://i.imgur.com/9gq8k25.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 6:
        embed.set_image(url="https://i.imgur.com/vSmGhGW.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 7:
        embed.set_image(url="https://i.imgur.com/1UJev0d.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 8:
        embed.set_image(url="https://i.imgur.com/2vfOEKZ.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 9:
        embed.set_image(url="https://i.imgur.com/vtDEhWB.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 10:
        embed.set_image(url="https://i.imgur.com/zIyeGTa.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 11:
        embed.set_image(url="https://i.imgur.com/GBKovkx.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 12:
        embed.set_image(url="https://i.imgur.com/OIoGGct.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 13:
        embed.set_image(url="https://i.imgur.com/QS6yFgZ.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 14:
        embed.set_image(url="https://i.imgur.com/Z07ta5J.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 15:
        embed.set_image(url="https://i.imgur.com/WB8LpT5.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 16:
        embed.set_image(url="https://i.imgur.com/mKwwOnc.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 17:
        embed.set_image(url="https://i.imgur.com/0QZCgMP.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 18:
        embed.set_image(url="https://i.imgur.com/S2Rgjlo.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 19:
        embed.set_image(url="https://i.imgur.com/yzkDGqk.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 20:
        embed.set_image(url="https://i.imgur.com/yupLbnj.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 21:
        embed.set_image(url="https://i.imgur.com/G1R1vZd.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 22:
        embed.set_image(url="https://i.imgur.com/mamFxFC.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 23:
        embed.set_image(url="https://i.imgur.com/NX0dJvE.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 24:
        embed.set_image(url="https://i.imgur.com/OuPJqcx.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 25:
        embed.set_image(url="https://i.imgur.com/1jUDYK8.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 26:
        embed.set_image(url="https://i.imgur.com/F3TtqoP.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 27:
        embed.set_image(url="https://i.imgur.com/spNANjO.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 28:
        embed.set_image(url="https://i.imgur.com/bPiLOaz.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 29:
        embed.set_image(url="https://i.imgur.com/6ehrsMQ.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 30:
        embed.set_image(url="https://i.imgur.com/1YBuo7g.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 31:
        embed.set_image(url="https://i.imgur.com/vJvTgPs.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 32:
        embed.set_image(url="https://i.imgur.com/5gQayVl.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 33:
        embed.set_image(url="https://i.imgur.com/Z1Q73LN.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 34:
        embed.set_image(url="https://i.imgur.com/RHsQmiN.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 35:
        embed.set_image(url="https://i.imgur.com/sfIcE2R.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 36:
        embed.set_image(url="https://i.imgur.com/0YK0ILZ.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 37:
        embed.set_image(url="https://i.imgur.com/gIMSv9x.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 38:
        embed.set_image(url="https://i.imgur.com/xd1xwiT.png")
        await ctx.message.channel.send(embed=embed)
    elif msg == 39:
        embed.set_image(url="https://i.imgur.com/DpZHG2D.jpg")
        await ctx.message.channel.send(embed=embed)
    elif msg == 40:
        embed.set_image(url="https://i.imgur.com/OhpQosJ.jpg")
        await ctx.message.channel.send(embed=embed)
    else:
        msg = str(msg)
        await ctx.message.channel.send(msg + " 번호는 없습니다")
        embed.set_image(url="https://i.imgur.com/cmSfQey.gif")
        await ctx.message.channel.send(embed=embed)

# @client.command()
# async def 사진검사(ctx):
#     embed = discord.Embed(imestamp=ctx.message.created_at,color=0x62c1cc)
#     img1 = "https://lh3.googleusercontent.com/proxy/07Uv8EaUpJSts1SYjA7ZpxnjVqXRlAirIv3umRlSVY4xCjzBdg5Eb6MnPQrMKkYg6435sINGbxXOo9jK5Sx1O2-hawVxqrl-W9J1qOlhVjljZ-kdO76JqkieGuSts2N4q8uPEFcDqPwBHmo4yX6JOs7MbZK2cn2tdpgzn6HDVIom9qUzOQ"
#     img2 = "https://2.gall-img.com/tdgall/files/attach/images/82/598/504/085/30637989dd98ccb51427279dca628024.jpg"
#     img3 = "https://upload.inven.co.kr/upload/2014/12/15/bbs/i4188200932.jpg"
#     img4 = "https://t1.daumcdn.net/cfile/blog/20457E4E4EC73F5215"
#     img5 = "https://t1.daumcdn.net/cfile/blog/17752B3E50ADEB3B15?original"
#     img6 = "https://lh3.googleusercontent.com/proxy/gFiZWmN41-R2aBUCLaPKq9wdmevKE_bEqkTTcCmSq_iZvxBWwPUO-cT8yPi6EzjDM6jcGdnMrkRz5zMrEGSGY51eGMJ5pkt6QHuVjRwYt5dHJ8j3_x74I5a8-nmQ9dHI3SvBi3EabE2iXS6UVzWV0EBVeu5NCXvSHWgpYWI1OnPoRUwUjh_DzV02Me11pwATuzItCgtSUsJeeWYNf3mMvdeSWaNFDdDEkprc2eoTm2mHEqr2cRfKOHn0iQbFWHmsvuS79TAn6iCxMqWNTmUnEN95Pg"
#     img7 = "https://lh3.googleusercontent.com/proxy/nYBwZDE6EnNBtDAP8Adn4z25y6cmdcIjRYr66gulMFlmw0WGKvb1naidSV1n8JVQ_jYKQuymP3SQHkcb94ajSWkftPiK-tXAzysu85hOUvIuBTRd6PRwV6uEExIrsw838h5kiiyeIStFLXcnQvKrqe_c8-jCmsBfriLf2w"
#     img8 = "https://lh3.googleusercontent.com/proxy/35WG5DG-PHXbINMQWggqWm7HJtEDBRsvLFN2rY13py8sQYJRgYFWwG0F-ePrwKVbeyIcpydbvuySKwtFlBZm5JMWe6--Cm9ofQ0LBX-kVS_zj6D0BS002OxfDscIrt9REx1_L71fC3FLozTTOI7kPCVQz-1aGCKtPCCk3ZS_YXdwnpWE5n0kn6U"
#     img9 = "https://obj-sg.thewiki.kr/data/4f494146796e42722e6a7067.jpg"
#     img10 = "https://pbs.twimg.com/media/Dux6NxMUcAA3w8t.png"
#     img11 = "https://pbs.twimg.com/media/EirkKsBXkAEnKjC.jpg"
#     img12 = "https://i.pinimg.com/originals/18/a9/50/18a950e2030611b94c89663ab2abfe3e.png"
#     img13 = "https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfile1.uf.tistory.com%2Fimage%2F22388D4D578768FD1AC52A"
#     img14 = "https://lh3.googleusercontent.com/proxy/jG_5EmAcqLpYKZn7DWT_NHW_QzeVzKnCpSc8HS8YseV53SNdJHgDJ0NJpyfh_gLYtWIZ94W5V7g5SgjQ4uW-Q36eW879GMGA8_TluCVnJtzzkvLzVCuCB3b4_w"
#     img15 = "http://thumbnail.egloos.net/460x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557cc76d34540.jpg"
#     img16 = "http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201506/14/56/f0027756_557cc7d263220.png"
#     img17 = "https://file.namu.moe/file/c2790d5985eae82cd1199a4cba2101c1424b45ac4df63d1f0c6f3c69850dfb22"
#     img18 = "https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfile29.uf.tistory.com%2Fimage%2F2629723B57879ACB1FA1EB"
#     img19 = "http://thumbnail.egloos.net/460x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557ccf7e10e07.png"
#     img20 = "http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201506/14/56/f0027756_557cc64902cfd.png"
#     img21 = "https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfile28.uf.tistory.com%2Fimage%2F266A3E4057879DA80FC421"
#     img22 = "http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201506/14/56/f0027756_557ccaf021449.jpg"
#     img23 = "http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557cce0cbab0a.jpg"
#     img24 = "http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201506/14/56/f0027756_557cce4f990e6.png"
#     img25 = "http://thumbnail.egloos.net/600x0/http://pds26.egloos.com/pds/201506/14/56/f0027756_557cd1c881a84.png"
#     img26 = "http://thumbnail.egloos.net/600x0/http://pds27.egloos.com/pds/201506/14/56/f0027756_557cd2415789d.jpg"
#     img27 = "http://thumbnail.egloos.net/600x0/http://pds26.egloos.com/pds/201506/14/56/f0027756_557cd35567aa4.jpg"
#     img28 = "http://thumbnail.egloos.net/600x0/http://pds26.egloos.com/pds/201506/14/56/f0027756_557cd3e751602.jpg"
#     img29 = "http://thumbnail.egloos.net/600x0/http://pds27.egloos.com/pds/201506/14/56/f0027756_557cd4481bdb2.png"
#     img30 = "http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557cdf9b6e7cb.jpg"
#     img31 = "http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201506/14/56/f0027756_557cd4d68991d.png"
#     img32 = "http://thumbnail.egloos.net/600x0/http://pds27.egloos.com/pds/201506/14/56/f0027756_557cd58604c51.png"
#     img33 = "http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557cd65cae8bb.png"
#     img34 = "http://thumbnail.egloos.net/600x0/http://pds26.egloos.com/pds/201506/14/56/f0027756_557ce159df55f.jpg"
#     img35 = "http://thumbnail.egloos.net/600x0/http://pds27.egloos.com/pds/201506/14/56/f0027756_557cd6c961e40.jpg"
#     img36 = "http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201506/14/56/f0027756_557cd6f613845.png"
#     img37 = "http://thumbnail.egloos.net/600x0/http://pds26.egloos.com/pds/201506/14/56/f0027756_557cda10251d8.png"
#     img38 = "http://pds26.egloos.com/pds/201506/14/56/f0027756_557cd8e6e363a.png"
#     img39 = "https://appzzang.me/data/file/hot_freeboard/thumb-31222651_HkzS9txX_czyscjl_800x974.jpg"
#     img40 = "https://c.wallhere.com/photos/1c/8c/anime_anime_girls_bikini_beach_feet_legs_blue_hair_blue_eyes-275636.jpg!d"
#     li = []
#     li.append(img1)
#     li.append(img2)
#     li.append(img3)
#     li.append(img4)
#     li.append(img5)
#     li.append(img6)
#     li.append(img7)
#     li.append(img8)
#     li.append(img9)
#     li.append(img10)
#     li.append(img11)
#     li.append(img12)
#     li.append(img13)
#     li.append(img14)
#     li.append(img15)
#     li.append(img16)
#     li.append(img17)
#     li.append(img18)
#     li.append(img19)
#     li.append(img20)
#     li.append(img21)
#     li.append(img22)
#     li.append(img23)
#     li.append(img24)
#     li.append(img25)
#     li.append(img26)
#     li.append(img27)
#     li.append(img28)
#     li.append(img29)
#     li.append(img30)
#     li.append(img31)
#     li.append(img32)
#     li.append(img33)
#     li.append(img34)
#     li.append(img35)
#     li.append(img36)
#     li.append(img37)
#     li.append(img38)
#     li.append(img39)
#     li.append(img40)    
#     await ctx.message.channel.send("약 40초 정도 소요됩니다.")
#     time.sleep(3)
#     for j in range(len(li)):
#         embed = discord.Embed(imestamp=ctx.message.created_at,color=0x62c1cc)
#         embed.set_image(url=li[j])
#         await ctx.message.channel.send(j+1)
#         await ctx.message.channel.send(embed=embed)
#         time.sleep(1)
#     await ctx.message.channel.send("검사종료")


client.run(token)
