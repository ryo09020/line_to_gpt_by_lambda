# line_to_gpt_by_lambda

# 機能
LINEでgpt-4oと会話できる！
作った目的としてはfine-tuningモデルをもっと楽に触れるようにしたい！から私は自分の情報を覚えさせた人格クローンを作ったのでそれと日常的に会話するために制作。

# 環境
python3.9
なぜか知らないけどpython3.11だとlayer設定しても`no module error`になる。。。

# 使用方法
- まずはawsのlambdaでアプリを作成してlambda.pyの中身をawsのlambda関数のlambda_function.pyにそのまま書く。(環境変数は各自設定してね)
  
- 次にlayerを定めます。lambdaにはターミナルがないので`pip install openai`とかができないのでこのライブラリのzipファイルをlayerに追加する必要があります。そのzipファイルが`linesdk-openai39py~.zip`です。このファイルをダウンロードしてそのままlayerにアップするとopen-aiとline-sdk-botの2つのライブラリを使用できるようになります。
