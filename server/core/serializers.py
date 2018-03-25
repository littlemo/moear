from rest_framework import serializers


class MetaListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        '''将传入的dict数据转换为符合数据模型的list形式'''
        data_dict = data
        data_list = []

        for (k, v) in data_dict.items():
            data_list.append({
                'name': k,
                'value': str(v),
            })

        return super().to_internal_value(data_list)

    def to_representation(self, instance):
        '''将输出的实例转成dict形式'''
        data_list = super().to_representation(instance)

        data_dict = {}
        for d in data_list:
            data_dict[d.get('name')] = d.get('value')

        return data_dict

    @property
    def data(self):
        return self.to_representation(self.instance)
