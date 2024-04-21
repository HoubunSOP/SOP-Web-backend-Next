import json

from schemas.external.bilibili import CVList

json_data = """
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "articles": [
      {
        "id": 33297251,
        "category": {
          "id": 15,
          "parent_id": 3,
          "name": "日常"
        },
        "categories": [
          {
            "id": 3,
            "parent_id": 0,
            "name": "生活"
          },
          {
            "id": 15,
            "parent_id": 3,
            "name": "日常"
          }
        ],
        "title": "摇曳露营现实体验指南",
        "summary": "免责声明：本文提供的一切户外知识仅供参考。户外情况复杂多变，各位读者在实际露营以及进行其他活动时根据实际情况做出行动。作者，作者所属的组织，并不保证，声明，或暗指本文的内容适合每个人，每种情况或目的，对其中可能存在的错误或者疏失不负任何责任。本文适用于娱乐休闲活动，以及针对成年读者。在尝试任何新活动之前，确保你清楚自身的局限性和活动存在的风险。本文所讲内容不能用来取代经验丰富的专家或户外运动专业人士做的判断和建议。   使用或者操作本文提到的任何工具和设备时，均应遵照相关使用说明。若设备制造商没有推荐本文",
        "banner_url": "",
        "template_id": 4,
        "state": 0,
        "author": {
          "mid": 1585955812,
          "name": "芳文观星台",
          "face": "https://i1.hdslb.com/bfs/face/8b25c5abe3d012c0033d43372e6880ade4a125b7.jpg",
          "pendant": {
            "pid": 0,
            "name": "",
            "image": "",
            "expire": 0
          },
          "official_verify": {
            "type": -1,
            "desc": ""
          },
          "nameplate": {
            "nid": 60,
            "name": "有爱萌新",
            "image": "https://i2.hdslb.com/bfs/face/51ca16136e570938450bca360f28761ceb609f33.png",
            "image_small": "https://i0.hdslb.com/bfs/face/9abfa4769357f85937782c2dbc40fafda4f57217.png",
            "level": "普通勋章",
            "condition": "当前持有粉丝勋章最高等级>=5级"
          },
          "vip": {
            "type": 2,
            "status": 1,
            "due_date": 0,
            "vip_pay_type": 0,
            "theme_type": 0,
            "label": {
              "path": "http://i0.hdslb.com/bfs/vip/label_annual.png",
              "text": "年度大会员",
              "label_theme": "annual_vip"
            },
            "avatar_subscript": 1,
            "nickname_color": "#FB7299"
          }
        },
        "reprint": 1,
        "image_urls": [
          "https://i0.hdslb.com/bfs/article/504082b8c2e0c1347d3974e50b15d8e51585955812.jpg"
        ],
        "publish_time": 1710858556,
        "ctime": 1710858556,
        "mtime": 1711254913,
        "stats": {
          "view": 5506,
          "favorite": 66,
          "like": 202,
          "dislike": 0,
          "reply": 7,
          "share": 0,
          "coin": 4,
          "dynamic": 0
        },
        "attributes": 128,
        "words": 14300,
        "origin_image_urls": [
          "https://i0.hdslb.com/bfs/article/504082b8c2e0c1347d3974e50b15d8e51585955812.jpg"
        ],
        "list": null,
        "is_like": false,
        "media": {
          "score": 0,
          "media_id": 0,
          "title": "",
          "cover": "",
          "area": "",
          "type_id": 0,
          "type_name": "",
          "spoiler": 0
        },
        "apply_time": "",
        "check_time": "",
        "original": 1,
        "act_id": 0,
        "dispute": null,
        "authenMark": null,
        "cover_avid": 0,
        "top_video_info": null,
        "type": 3,
        "check_state": 0,
        "origin_template_id": 4
      },
      {
        "id": 32280884,
        "category": {
          "id": 15,
          "parent_id": 3,
          "name": "日常"
        },
        "categories": [
          {
            "id": 3,
            "parent_id": 0,
            "name": "生活"
          },
          {
            "id": 15,
            "parent_id": 3,
            "name": "日常"
          }
        ],
        "title": "【观星台汉化】饿肚子少女和侦探 - 03（客串）",
        "summary": "20岁深陷于中二病（？）的律歌一直憧憬着小说「癫狂侦探」里的情景，同时也是一名笨手笨脚的冒牌侦探，而吃货高中生音都则被其强行拉拢成为了助手。如此一对靠不住的组合，她们二人此后作为名侦探享誉盛名，成功捉拿世纪怪盗的那天真的会到来吗！由年轻侦探们打造的温馨推理搞笑漫画！ [图片] [图片] [图片] [图片] [图片] [图片] [图片] [图片] [图片] [图片] [图片] ",
        "banner_url": "",
        "template_id": 4,
        "state": 7,
        "author": {
          "mid": 1585955812,
          "name": "芳文观星台",
          "face": "https://i1.hdslb.com/bfs/face/8b25c5abe3d012c0033d43372e6880ade4a125b7.jpg",
          "pendant": {
            "pid": 0,
            "name": "",
            "image": "",
            "expire": 0
          },
          "official_verify": {
            "type": -1,
            "desc": ""
          },
          "nameplate": {
            "nid": 60,
            "name": "有爱萌新",
            "image": "https://i2.hdslb.com/bfs/face/51ca16136e570938450bca360f28761ceb609f33.png",
            "image_small": "https://i0.hdslb.com/bfs/face/9abfa4769357f85937782c2dbc40fafda4f57217.png",
            "level": "普通勋章",
            "condition": "当前持有粉丝勋章最高等级>=5级"
          },
          "vip": {
            "type": 2,
            "status": 1,
            "due_date": 0,
            "vip_pay_type": 0,
            "theme_type": 0,
            "label": {
              "path": "http://i0.hdslb.com/bfs/vip/label_annual.png",
              "text": "年度大会员",
              "label_theme": "annual_vip"
            },
            "avatar_subscript": 1,
            "nickname_color": "#FB7299"
          }
        },
        "reprint": 0,
        "image_urls": [
          "https://i0.hdslb.com/bfs/article/a9f9a16eeda9dfd0e932fe21b9d86f201585955812.jpg"
        ],
        "publish_time": 1709194430,
        "ctime": 1709194430,
        "mtime": 1709195496,
        "stats": {
          "view": 4579,
          "favorite": 9,
          "like": 114,
          "dislike": 0,
          "reply": 1,
          "share": 0,
          "coin": 2,
          "dynamic": 0
        },
        "words": 133,
        "origin_image_urls": [
          "https://i0.hdslb.com/bfs/article/a9f9a16eeda9dfd0e932fe21b9d86f201585955812.jpg"
        ],
        "list": null,
        "is_like": false,
        "media": {
          "score": 0,
          "media_id": 0,
          "title": "",
          "cover": "",
          "area": "",
          "type_id": 0,
          "type_name": "",
          "spoiler": 0
        },
        "apply_time": "",
        "check_time": "",
        "original": 0,
        "act_id": 0,
        "dispute": null,
        "authenMark": null,
        "cover_avid": 0,
        "top_video_info": null,
        "type": 3,
        "check_state": 0,
        "origin_template_id": 4
      }
    ],
    "pn": 1,
    "ps": 100,
    "count": 27
  }
}
"""


def get_articles_ids(jsondata: CVList):
    return [article.id for article in jsondata.data.articles]


if __name__ == "__main__":
    json_c = json.loads(json_data)
    cvlist = CVList.parse_obj(json_c)
    print(get_articles_ids(cvlist))
