import pke
extractor = pke.unsupervised.MultipartiteRank()
# language='ja' とする
extractor.load_document(input='テスト実施', language='ja', normalization=None)
