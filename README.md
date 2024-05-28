# line_to_gpt_by_lambda

# 機能
LINEでgpt-4oと会話しよう！

# 使用方法
- まずはawsのlambdaでアプリを作成してlambda.pyの中身をawsのlambda関数のlambda_function.pyにそのまま書く。
- 次にlayerを定めます。lambdaにはターミナルがないので'pip install openai'とかができないのでこのライブラリのzipファイルをlayerに追加する必要があります。そのzipファイルが
