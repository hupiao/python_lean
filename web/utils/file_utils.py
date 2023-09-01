import logging
import geoip2.database


class GeoIP(object):
    """
    地理信息查询
    """

    def __init__(self):
        self.db = geoip2.database.Reader('./GeoLite2-City.mmdb')

    def close(self):
        self.db.close()

    def city(self, ip, locales='en'):
        """
        查询IP地址对应的地理名
        :param ip:
        :param locales:
        :return:
        """
        _country, _subdivision, _city = '', '', ''
        try:
            city = self.db.city(ip)
            print(city)
            print(city.country.names)
            _country = city.country.names.get(locales, '')  # 国家
            _subdivision = city.subdivisions.most_specific.names.get(locales, '')  # 省
            _city = city.city.names.get(locales, '')  # 市
        except geoip2.errors.AddressNotFoundError as ex:  # noqa
            logging.exception('geoip failure')
        except Exception as ex:  # noqa
            logging.exception('geoip exception')

        return (_country, _subdivision, _city)

    def location(self, ip):
        """
        查询IP地址对应的地理位置[经度，纬度]
        :param ip:
        :return:
        """
        _longitude, _latitude = '', ''
        try:
            city = self.db.city(ip)
            _longitude = city.location.longitude  # 经度
            _latitude = city.location.latitude  # 纬度
        except geoip2.errors.AddressNotFoundError as ex:  # noqa
            logging.exception('geoip failure')
        except Exception as ex:  # noqa
            logging.exception('geoip exception')

        return [_longitude, _latitude]


print(GeoIP().city("171.43.155.15"))
a = {'city': {'geoname_id': 1791247,
              'names': {'de': 'Wuhan', 'en': 'Wuhan', 'es': 'Wuhan', 'fr': 'Wuhan', 'ja': '武漢市', 'pt-BR': 'Wuhan',
                        'ru': 'Ухань', 'zh-CN': '武汉'}}, 'continent': {'code': 'AS', 'geoname_id': 6255147,
                                                                      'names': {'de': 'Asien', 'en': 'Asia',
                                                                                'es': 'Asia', 'fr': 'Asie', 'ja': 'アジア',
                                                                                'pt-BR': 'Ásia', 'ru': 'Азия',
                                                                                'zh-CN': '亚洲'}},
     'country': {'geoname_id': 1814991, 'iso_code': 'CN',
                 'names': {'de': 'China', 'en': 'China', 'es': 'China', 'fr': 'Chine', 'ja': '中国', 'pt-BR': 'China',
                           'ru': 'Китай', 'zh-CN': '中国'}},
     'location': {'accuracy_radius': 100, 'latitude': 30.5856, 'longitude': 114.2665, 'time_zone': 'Asia/Shanghai'},
     'registered_country': {'geoname_id': 1814991, 'iso_code': 'CN',
                            'names': {'de': 'China', 'en': 'China', 'es': 'China', 'fr': 'Chine', 'ja': '中国',
                                      'pt-BR': 'China', 'ru': 'Китай', 'zh-CN': '中国'}},
     'subdivisions': [
        {'geoname_id': 1806949, 'iso_code': 'HB',
         'names': {'de': 'Hubei', 'en': 'Hubei', 'es': 'Hubei', 'fr': 'Province de Hubei', 'ja': '湖北省',
                   'pt-BR': 'Hubei', 'ru': 'Хубэй', 'zh-CN': '湖北省'}}],
     'traits': {'ip_address': '171.43.155.15', 'prefix_len': 19}}, ['en']
