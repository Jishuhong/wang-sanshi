#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ToTng 网站图片裁剪脚本
从桌面 M 文件夹的原始图片中裁剪出：
1. 枪皮图片（独立每把枪）
2. 英雄卡面
3. ToTng 头像（从昵称图提取文字部分）
"""

from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, 'assets', 'raw')
SKINS_DIR = os.path.join(BASE_DIR, 'assets', 'skins')
CARDS_DIR = os.path.join(BASE_DIR, 'assets', 'cards')
DATA_DIR = os.path.join(BASE_DIR, 'assets', 'data')

def ensure_dirs():
    """确保输出目录存在"""
    os.makedirs(SKINS_DIR, exist_ok=True)
    os.makedirs(CARDS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

def crop_gun_skins_1():
    """
    裁剪枪皮 1.jpg - 混沌序曲系列 5 把枪
    图片尺寸：1080x2376，纵向排列，每把枪约占顶部区域的 1/5
    每张包含标题 + 枪图，需要裁掉两侧背景只保留枪的主体
    """
    img = Image.open(os.path.join(RAW_DIR, '枪皮 1.jpg'))
    width, height = img.size
    print(f"枪皮 1.jpg 尺寸：{width}x{height}")

    # 5 把混沌序曲枪皮，从上到下排列
    # 每张区域高度约 420px，但标题在上面约 100px，枪体在下面约 280px
    skin_names = ['冥驹', '狂徒', '鬼魅', '幻影', '骇灵']

    for i, name in enumerate(skin_names):
        # 每个皮肤区域起始位置
        y_start = i * (height // 5)
        y_end = (i + 1) * (height // 5)

        # 裁剪单个皮肤区域
        skin_region = img.crop((0, y_start, width, y_end))

        # 进一步裁剪，去掉标题，只保留枪体部分（假设枪体在区域的下半部分）
        # 或者保留整个区域让 CSS 处理
        skin_region.save(os.path.join(SKINS_DIR, f'chroma_{name}.jpg'), 'JPEG', quality=90)
        print(f"  → 已保存：chroma_{name}.jpg")

    img.close()

def crop_gun_skins_2():
    """
    裁剪枪皮 2.jpg - RG Collection 2 把枪 + 2 张英雄卡面
    图片尺寸：1080x2376
    """
    img = Image.open(os.path.join(RAW_DIR, '枪皮 2.jpg'))
    width, height = img.size
    print(f"枪皮 2.jpg 尺寸：{width}x{height}")

    # 分析图片结构，假设前部分是枪皮，后部分是卡面
    # RG 狂徒和 RG 冥驹在前 2 个区域，Sova 和 Killjoy 卡面在后

    gun_skins = ['RG_狂徒', 'RG_冥驹']

    for i, name in enumerate(gun_skins):
        y_start = i * (height // 4)
        y_end = (i + 1) * (height // 4)

        skin_region = img.crop((0, y_start, width, y_end))
        skin_region.save(os.path.join(SKINS_DIR, f'{name}.jpg'), 'JPEG', quality=90)
        print(f"  → 已保存：{name}.jpg")

    # 英雄卡面在下方区域
    card_names = ['Sova', 'Killjoy']
    for i, name in enumerate(card_names):
        y_start = 2 * (height // 4) + i * (height // 4)
        y_end = min((i + 3) * (height // 4), height)

        card_region = img.crop((0, y_start, width, y_end))
        card_region.save(os.path.join(CARDS_DIR, f'{name}.jpg'), 'JPEG', quality=90)
        print(f"  → 已保存：{name}.jpg")

    img.close()

def crop_avatar():
    """
    从 71627bd9...jpg（昵称主页图）中提取 "ToTng" 文字作为头像
    这个文件是 ToTng 昵称主页 + 英雄卡面
    """
    img = Image.open(os.path.join(RAW_DIR, '71627bd93330a606e978858ed4f5d555.jpg'))
    width, height = img.size
    print(f"\n7162 昵称图尺寸：{width}x{height}")

    # 假设 ToTng 文字在图的中间上方位置
    # 根据常见布局，昵称通常在顶部中央
    # 裁剪中间上方的文字区域作为头像
    avatar_x1 = width * 0.3
    avatar_y1 = height * 0.15
    avatar_x2 = width * 0.7
    avatar_y2 = height * 0.35

    avatar = img.crop((int(avatar_x1), int(avatar_y1), int(avatar_x2), int(avatar_y2)))
    # 调整尺寸到正方形
    new_size = 300
    avatar_resized = avatar.resize((new_size, new_size), Image.Resampling.LANCZOS)
    avatar_resized.save(os.path.join(DATA_DIR, 'avatar_totng.jpg'), 'JPEG', quality=95)
    print(f"  → 已保存：avatar_totng.jpg")

    img.close()

def prepare_data_images():
    """
    准备数据展示图片 - 直接使用原图或简单裁剪关键区域
    """
    # 铁臂数据图 - 5cb7...jpg
    img = Image.open(os.path.join(RAW_DIR, '5cb745e776871a2efeae005d2606405c.jpg'))
    w, h = img.size
    # 裁剪显示 KDA、胜率等核心数据的区域
    data_area = img.crop((0, h//4, w, h//2))
    data_area.save(os.path.join(DATA_DIR, 'stats_kda.jpg'), 'JPEG', quality=90)
    print("已保存 stats_kda.jpg")
    img.close()

    # 混沌序曲卡面列表图 - 678a...jpg
    img = Image.open(os.path.join(RAW_DIR, '678a5a8a12e2cd057389915b0b75e1d6.jpg'))
    cards_area = img.crop((0, h*0.3, w, h*0.7))
    cards_area.save(os.path.join(DATA_DIR, 'card_collection.jpg'), 'JPEG', quality=90)
    print("已保存 card_collection.jpg")
    img.close()

    # 击杀助攻死亡数据图 - 829e...jpg
    img = Image.open(os.path.join(RAW_DIR, '829e07090ec2bf691d4810228cbfaaa9.jpg'))
    kd_area = img.crop((0, h*0.2, w, h*0.5))
    kd_area.save(os.path.join(DATA_DIR, 'stats_kd.jpg'), 'JPEG', quality=90)
    print("已保存 stats_kd.jpg")
    img.close()

def main():
    print("=" * 50)
    print("ToTng 网站图片裁剪工具")
    print("=" * 50)

    ensure_dirs()
    print(f"\n目录结构:")
    print(f"  RAW: {RAW_DIR}")
    print(f"  SKINS: {SKINS_DIR}")
    print(f"  CARDS: {CARDS_DIR}")
    print(f"  DATA: {DATA_DIR}\n")

    print("开始裁剪枪皮图片...")
    try:
        crop_gun_skins_1()
        crop_gun_skins_2()
    except Exception as e:
        print(f"枪皮裁剪出错：{e}")

    print("\n准备头像和数据图片...")
    try:
        crop_avatar()
        prepare_data_images()
    except Exception as e:
        print(f"头像/数据裁剪出错：{e}")

    print("\n" + "=" * 50)
    print("完成!")
    print("=" * 50)

if __name__ == '__main__':
    main()
