class Filter_Init():
    def __init__(self,app):
        
        @app.template_filter()
        def get_dict(dict):
            r=''
            for k,v in dict.items():
                r+=f'{k}:{v}  '
            return r
