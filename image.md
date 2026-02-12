API 使用示例（需要使用流式）
文生图
curl -X POST "https://api.haoapi.top/v1/chat/completions" \
  -H "Authorization: Bearer XXXX" \   # 此处需要填写APIKEY
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.0-pro-image-landscape",
    "messages": [
      {
        "role": "user",
        "content": "一只可爱的猫咪在花园里玩耍"
      }
    ],
    "stream": true
  }'
图生图
curl -X POST "https://api.haoapi.top/v1/chat/completions" \
  -H "Authorization: Bearer XXXX" \   # 此处需要填写APIKEY
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.0-pro-image-landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "将这张图片变成水彩画风格"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<base64_encoded_image>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'

  模型：
gemini-3.0-pro-image-landscape	图/文生图	横屏
gemini-3.0-pro-image-portrait	图/文生图	竖屏
gemini-3.0-pro-image-landscape-2k	图/文生图	横屏  2k
gemini-3.0-pro-image-portrait-2k	图/文生图	竖屏  2k
gemini-3.0-pro-image-landscape-4k	图/文生图	横屏  4k
gemini-3.0-pro-image-portrait-4k	图/文生图	竖屏  4k



完整请求  第一种：
curl -X POST "http://flow.lyvideo.top/v1/chat/completions" -H "Authorization: Bearer han1234" -H "Content-Type: application/json" -d '{
  "model": "gemini-3.0-pro-image-landscape-2k",
  "messages": [
    {
      "role": "user",
      "content": "一只可爱的猫咪在花园里玩耍"
    }
  ],
  "stream": true
}'
data: {"id": "chatcmpl-1770892297", "object": "chat.completion.chunk", "created": 1770892297, "model": "flow2api", "choices": [{"index": 0, "delta": {"role": "assistant", "reasoning_content": "✨ 图片生成任务已启动\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770892297", "object": "chat.completion.chunk", "created": 1770892297, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "初始化生成环境...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770892297", "object": "chat.completion.chunk", "created": 1770892297, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "正在生成图片...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770892322", "object": "chat.completion.chunk", "created": 1770892322, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "正在放大图片到 2K...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770892337", "object": "chat.completion.chunk", "created": 1770892337, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "✅ 图片已放大到 2K\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770892337", "object": "chat.completion.chunk", "created": 1770892337, "model": "flow2api", "choices": [{"index": 0, "delta": {"content": "![Generated Image](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEBLAEsAAD/6zZeSlAAAQAAAAEAADZUanVtYgAAAB5qdW1kYzJwYQARABCAAACqADibcQNjMnBhAAAAF9pqdW1iAAAAR2p1bWRjMm1hABEAEIAAAKoAOJtxA3VybjpjMnBhOmNhZDU4YmYxLTFhMjQtZTI5My1kNDllLTQwOGUxY2MyYjY5NQAAABODanVtYgAAAChqdW1kYzJjcwARABCAAACqADibcQNjMnBhLnNpZ25hdHVyZQAAABNTY2JvctKEWQauogEmGCGCWQPCMIIDvjCCA0SgAwIBAgITf8DFXrYCzoMPnf3QSrAMRZ64JjAKBggqhkjOPQQDAzBRMQswCQYDVQQGEwJVUzETMBEGA1UECgwKR29vZ2xlIExMQzEtMCsGA1UEAwwkR29vZ2xlIEMyUEEgTWVkaWEgU2VydmljZXMgMVAgSUNBIEczMB4XDTI1MTAzMDIyMzQ0N1oXDTI2MTAyNTIyMzQ0NlowazELMAkGA1UEBhMCVVMxEzARBgNVBAoTCkdvb2dsZSBMTEMxHDAaBgNVBAsTE0dvb2dsZSBTeXN0ZW0gNjAwMzIxo4Lnkmrpyu2vdu0fMTw8FFOVSUrO7T0V76bWT6Xve9uqbPWNM8V6lYfDJoJvDR0bU/D9k1rYaPDdKn9oyQQoqHYhKGJz8/lEkBGBkkb7r+QfDrRtV8S+K77xv8AFbQ7fTJdPhtn8KaVa4U2kLIWmknVMiS4mLHaZCCGO9FCquPuvwP4F0PS7YrrOqWusXJRd0txdW0obairjBldgg2hjuJ3ME4AjOfN/jBquj6NAzae9gZFJSzSKa0+d/lG0qsmQA21BgHcGxgDJH9G8bVKvBvAtTOHTdOOEoxbp1IwnKUIU2ox5IpK+sbcqT0ReA9hisXGhyNyhqpxsox0t0snve6au0uzZ5Z4htItWtL9tQlew0ZZPNtt2fNkbYChZmYsoG0YUqQoDBcgbj8vePPidPoMNxo+iRyTwRW1xbRiRd8bq8Th5AzFcLsXAZiS7OTnORXrKahNqdg8mp3quZiSkJuE2Ku3KgKXUAlQCVGQFXbwCwXxjxPYaf5d5IHgYtHOFDTR+YHA4ZSHIz0wThR98hsAD/L3injbEcUZ/h8dhMJiaEJVuapUnKTq1I86la0VyU4KOqj0W7ufW1HKjh5UYzjb3eVONmuj1vdvZtv8dz//2Q==)"}, "finish_reason": "stop"}]}

data: [DONE]



第二种：curl -X POST "http://flow.lyvideo.top/v1/chat/completions" -H "Authorization: Bearer han1234" -H "Content-Type: application/json" -d '{
  "model": "gemini-3.0-pro-image-landscape",   
  "messages": [
    {
      "role": "user",
      "content": "一只可爱的猫咪在花园里玩耍"
    }
  ],
  "stream": true
}'
data: {"id": "chatcmpl-1770915381", "object": "chat.completion.chunk", "created": 1770915381, "model": "flow2api", "choices": [{"index": 0, "delta": {"role": "assistant", "reasoning_content": "✨ 图片生成任务已启动\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770915381", "object": "chat.completion.chunk", "created": 1770915381, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "初始化生成环境...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770915381", "object": "chat.completion.chunk", "created": 1770915381, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "正在生成图片...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770915413", "object": "chat.completion.chunk", "created": 1770915413, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "缓存已关闭,正在返回源链接...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770915413", "object": "chat.completion.chunk", "created": 1770915413, "model": "flow2api", "choices": [{"index": 0, "delta": {"content": "![Generated Image](https://storage.googleapis.com/ai-sandbox-videofx/image/6a2e707a-6851-411b-ac73-d082f2c54762?GoogleAccessId=labs-ai-sandbox-videoserver-prod@system.gserviceaccount.com&Expires=1770937012&Signature=Hjt3ZqUImsh1vqSXd%2FWimbP5agwGi2XQ7UWSoFHnDmKK002PsJ3P9Z3SwWursIY2WU4DPdUZ62O6JW5%2BMNMeBhpaAf4S35LfB2KH90xshCWYgO%2BJk%2BFLnEmjLy3GutbvYqDWAIs8xPVi8K3c3XwnHy0tNU7yCIcMd1Wo6VloR0pLVyR0l2lLo6JpK9nT7COJ%2BuYC1S132YX9RZnQvHXdDyP0hCPMzkVLrOIcrA7VxRFi4BXRLyf%2BlucpPdwWJLXUWhXkR%2BGa33EC%2FsMZGmdm%2B9aYcC7rsIL6P%2BYhjYvo6X22%2B1GsJ4UQv3oFmrfdhx%2BgJPo%2Fdw5sjROV1skCrz9CCQ%3D%3D)"}, "finish_reason": "stop"}]}

data: [DONE]


