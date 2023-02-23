import paddlehub as hub

lac = hub.Module(name="lac")
test_text = ["吃饭没得"]

results = lac.cut(text=test_text, use_gpu=False, batch_size=1, return_tag=True)
print(results) #need version 2.0.0