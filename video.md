API调用方式
视频生成
文生视频
curl -X POST "https://hetang.lyvideo.top/v1/chat/completions" \
  -H "Authorization: Bearer XXXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_t2v_fast_landscape",
    "messages": [
      {
        "role": "user",
        "content": "一只小猫在草地上追逐蝴蝶"
      }
    ],
    "stream": true
  }'
首尾帧，可以首帧，也可以首尾帧，首帧就是传入一个图片
curl -X POST "https://hetang.lyvideo.top/v1/chat/completions" \
  -H "Authorization: Bearer XXXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "veo_3_1_i2v_s_fast_fl_landscape",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "从第一张图过渡到第二张图"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<首帧base64>"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,<尾帧base64>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'


模型：
veo_3_1_i2v_s_fast_fl   横屏  图生视频
veo_3_1_i2v_s_fast_portrait_fl   竖屏   图生视频
veo_3_1_t2v_fast_landscape   横屏  文生视频 
veo_3_1_t2v_fast_portrait  竖屏 文生视频 


模型测试结果汇总（二次测试更新）：
✅ 可用模型：
  veo_3_1_t2v_fast_landscape      横屏 文生视频       正常返回视频链接（重测恢复）
  veo_3_1_t2v_fast_portrait       竖屏 文生视频       正常返回视频链接
  veo_3_1_i2v_s_fast_fl           横屏 图生视频       正常返回视频链接
  veo_3_1_i2v_s_fast_portrait_fl  竖屏 图生视频       正常返回视频链接




完整请求  文生视频（成功示例 veo_3_1_t2v_fast_portrait）：
curl -X POST "https://hetang.lyvideo.top/v1/chat/completions" -H "Authorization: Bearer sk-P7EIz4dKi9UQG6Yed2qp74M45nU0A2ictnyOat4WKeoZW7wm" -H "Content-Type: application/json" -d '{
  "model": "veo_3_1_t2v_fast_portrait",
  "messages": [
    {
      "role": "user",
      "content": "一只小猫在草地上追逐蝴蝶"
    }
  ],
  "stream": true
}'
data: {"id": "chatcmpl-1770950164", "object": "chat.completion.chunk", "created": 1770950164, "model": "flow2api", "choices": [{"index": 0, "delta": {"role": "assistant", "reasoning_content": "✨ 视频生成任务已启动\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950164", "object": "chat.completion.chunk", "created": 1770950164, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "初始化生成环境...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950164", "object": "chat.completion.chunk", "created": 1770950164, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "TIER_TWO 账号自动切换到 ultra 模型: veo_3_1_t2v_fast_portrait_ultra\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950164", "object": "chat.completion.chunk", "created": 1770950164, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "提交视频生成任务...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950177", "object": "chat.completion.chunk", "created": 1770950177, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "视频生成中...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950180", "object": "chat.completion.chunk", "created": 1770950180, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 0%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950207", "object": "chat.completion.chunk", "created": 1770950207, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 3%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950233", "object": "chat.completion.chunk", "created": 1770950233, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 7%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950241", "object": "chat.completion.chunk", "created": 1770950241, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "缓存已关闭,正在返回源链接...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950241", "object": "chat.completion.chunk", "created": 1770950241, "model": "flow2api", "choices": [{"index": 0, "delta": {"content": "<video src='https://storage.googleapis.com/ai-sandbox-videofx/video/ce3d8279-f338-4ffa-915d-d192151a60c2?GoogleAccessId=labs-ai-sandbox-videoserver-prod@system.gserviceaccount.com&Expires=1770971838&Signature=ayuU1jCUzB0dHJInag9F1qhiy5HzcOKMtuvDlFeUlk%2B8bkeSMFFot%2BNM6LK9cKMFA93SzX0qVKWRBEgLRIsE9qPl6ZdpyEN6hU%2BsjoMugdc5Ya3%2BUqooTIAmyH0hl3VcMnKaqfEtUcnJWyIvlFoMngGs6%2FfV2JwMQy%2BBqgRYfPLswXJC1SWUCTN0LeQXz5BFYzjvG%2FTGFwdDda81cxqFwO%2BZECCPp6lU2NljVAchTc5Ts5LB3D5P0K9m7xZXGQcCgbPuKbQ%2BmnWLMK5aozZrqg4%2FHX%2FXu6hUMWXxoCf46ejjZ6EkDTFAqb2E4cSbwqsO2U5ehyYCFeEAjKi98AJJgA%3D%3D' controls style='max-width:100%'></video>"}, "finish_reason": "stop"}]}

data: {"id":"chatcmpl-1770950241","object":"chat.completion.chunk","created":1770950241,"model":"flow2api","system_fingerprint":"","choices":[],"usage":{"prompt_tokens":18,"completion_tokens":329,"total_tokens":347,"prompt_tokens_details":{"cached_tokens":0,"text_tokens":0,"audio_tokens":0,"image_tokens":0},"completion_tokens_details":{"text_tokens":0,"audio_tokens":0,"reasoning_tokens":0},"input_tokens":0,"output_tokens":0,"input_tokens_details":null,"claude_cache_creation_5_m_tokens":0,"claude_cache_creation_1_h_tokens":0}}

data: [DONE]


完整请求  文生视频（失败示例 veo_3_1_t2v_fast_landscape）：
curl -X POST "https://hetang.lyvideo.top/v1/chat/completions" -H "Authorization: Bearer sk-P7EIz4dKi9UQG6Yed2qp74M45nU0A2ictnyOat4WKeoZW7wm" -H "Content-Type: application/json" -d '{
  "model": "veo_3_1_t2v_fast_landscape",
  "messages": [
    {
      "role": "user",
      "content": "一只小猫在草地上追逐蝴蝶"
    }
  ],
  "stream": true
}'
data: {"id": "chatcmpl-1770950163", "object": "chat.completion.chunk", "created": 1770950163, "model": "flow2api", "choices": [{"index": 0, "delta": {"role": "assistant", "reasoning_content": "✨ 视频生成任务已启动\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950163", "object": "chat.completion.chunk", "created": 1770950163, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "初始化生成环境...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950163", "object": "chat.completion.chunk", "created": 1770950163, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "TIER_TWO 账号自动切换到 ultra 模型: veo_3_1_t2v_fast_ultra\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950163", "object": "chat.completion.chunk", "created": 1770950163, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "提交视频生成任务...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950171", "object": "chat.completion.chunk", "created": 1770950171, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "❌ 生成失败: Flow API request failed: HTTP Error 401: Request had invalid authentication credentials. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project.\n"}, "finish_reason": null}]}

data: {"id":"chatcmpl-1770950171","object":"chat.completion.chunk","created":1770950171,"model":"flow2api","system_fingerprint":"","choices":[],"usage":{"prompt_tokens":18,"completion_tokens":121,"total_tokens":139,"prompt_tokens_details":{"cached_tokens":0,"text_tokens":0,"audio_tokens":0,"image_tokens":0},"completion_tokens_details":{"text_tokens":0,"audio_tokens":0,"reasoning_tokens":0},"input_tokens":0,"output_tokens":0,"input_tokens_details":null,"claude_cache_creation_5_m_tokens":0,"claude_cache_creation_1_h_tokens":0}}

data: [DONE]


完整请求  图生视频（成功示例 veo_3_1_i2v_s_fast_fl）：
curl -X POST "https://hetang.lyvideo.top/v1/chat/completions" -H "Authorization: Bearer sk-P7EIz4dKi9UQG6Yed2qp74M45nU0A2ictnyOat4WKeoZW7wm" -H "Content-Type: application/json" -d '{
  "model": "veo_3_1_i2v_s_fast_fl",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "让这张图片动起来，小猫在草地上奔跑"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,<首帧base64>"
          }
        }
      ]
    }
  ],
  "stream": true
}'
data: {"id": "chatcmpl-1770950481", "object": "chat.completion.chunk", "created": 1770950481, "model": "flow2api", "choices": [{"index": 0, "delta": {"role": "assistant", "reasoning_content": "✨ 视频生成任务已启动\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950481", "object": "chat.completion.chunk", "created": 1770950481, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "初始化生成环境...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950481", "object": "chat.completion.chunk", "created": 1770950481, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "TIER_TWO 账号自动切换到 ultra 模型: veo_3_1_i2v_s_fast_ultra_fl\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950481", "object": "chat.completion.chunk", "created": 1770950481, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "上传首帧图片...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950492", "object": "chat.completion.chunk", "created": 1770950492, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "提交视频生成任务...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950505", "object": "chat.completion.chunk", "created": 1770950505, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "视频生成中...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950509", "object": "chat.completion.chunk", "created": 1770950509, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 0%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950535", "object": "chat.completion.chunk", "created": 1770950535, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 3%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950561", "object": "chat.completion.chunk", "created": 1770950561, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "生成进度: 7%\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950571", "object": "chat.completion.chunk", "created": 1770950571, "model": "flow2api", "choices": [{"index": 0, "delta": {"reasoning_content": "缓存已关闭,正在返回源链接...\n"}, "finish_reason": null}]}

data: {"id": "chatcmpl-1770950571", "object": "chat.completion.chunk", "created": 1770950571, "model": "flow2api", "choices": [{"index": 0, "delta": {"content": "<video src='https://storage.googleapis.com/ai-sandbox-videofx/video/c8fb621a-6da9-490a-8383-dcf06e39d41b?GoogleAccessId=labs-ai-sandbox-videoserver-prod@system.gserviceaccount.com&Expires=1770972169&Signature=Niq76Ol8xR%2BoldqL6R7RaZ1%2BNKlqcs8NjO3d2BZcbDxS1NBZBL6mOYGPQfb0gwiKT%2FR7aJGurX1qlY%2BKbip%2Bo4RnVj46Mf0YHyA6IH9aqrqcgs%2F%2B2%2BDJMDyQBdbz1xgJxvoIzIVb6AVptxhFuMBREKd%2BfMdcYHdNOSw0axoKPW4MxxuZXm7yg61FvZTeSqz80gagayf9x9CmnTMY96LCLQs%2Bb4qjIAZln7w7BS9g%2FjcKOitbkR9%2F5kTKnqm0sQPlMi2xo8A%2F6pPJfq0E2pj6RgrVker%2B75YF9E%2BAh5lWgJiuCGFJj9f059NUotXNUkYWCPJYdhOX9s0i1nf1DVWXzw%3D%3D' controls style='max-width:100%'></video>"}, "finish_reason": "stop"}]}

data: {"id":"chatcmpl-1770950571","object":"chat.completion.chunk","created":1770950571,"model":"flow2api","system_fingerprint":"","choices":[],"usage":{"prompt_tokens":542,"completion_tokens":377,"total_tokens":919,"prompt_tokens_details":{"cached_tokens":0,"text_tokens":0,"audio_tokens":0,"image_tokens":0},"completion_tokens_details":{"text_tokens":0,"audio_tokens":0,"reasoning_tokens":0},"input_tokens":0,"output_tokens":0,"input_tokens_details":null,"claude_cache_creation_5_m_tokens":0,"claude_cache_creation_1_h_tokens":0}}

data: [DONE]


完整请求  图生视频 4K（失败示例 veo_3_1_i2v_s_fast_portrait_ultra_fl_4k / veo_3_1_i2v_s_fast_ultra_fl_4k）：
返回结果：error code: 524（服务端超时）
