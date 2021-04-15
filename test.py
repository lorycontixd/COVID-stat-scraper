import subprocess

result = subprocess.run(["which","chromedriver"],capture_output=True)
out = result.stdout.decode("utf-8")
print(out,"  -  ",len(out))
