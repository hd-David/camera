import boto3
import json
import sys
import tempfile
import requests
#from register_camera import get_credentials

iot_client = boto3.client('iot')
iam_client = boto3.client('iam')
kinesisvideo_client = boto3.client('kinesisvideo')

certificates_what = {
    "certificateArn": "arn:aws:iot:eu-central-1:354231728084:cert/36cfc24c6c611767940ad7fc03e4bf505daefa7f940919ec08f73ae4a4114ce2",
    "certificateId": "36cfc24c6c611767940ad7fc03e4bf505daefa7f940919ec08f73ae4a4114ce2",
    "certificatePem": "-----BEGIN CERTIFICATE-----\nMIIDWTCCAkGgAwIBAgIUYcZDle8uIfI5fHBtWMxqcXkZzZUwDQYJKoZIhvcNAQEL\nBQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g\nSW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTIyMDUxMzA4MTAw\nM1oXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0\nZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAO9SFGATKkqFx7b4ZGju\ntJlCx3kXADYFjpJeCS+9SEVz6t9ooW/VoGylmnLjY6Ij9LtkJ7uUUQgahaFQCkg9\nPg5obse/1sEcJZIK6Aiy5wySCVQzFzKABkQSf2gb3y9O/iIQmj1iDXI2zEwel4wK\n3d6bwiB3U402IB+7YbBJ0atlmJOM5G/vhZ21fDEy+3purNcKO/kyGJHganthkXKZ\nUSqwgv3NF8eLkdsfCdoNIH0m72080iLcrHCON47ONv+tdNBOReRiDaiXx18r7OMA\npsHMH7usV/DsRsPU9VUvQtSyA/oYkWCZ5mLa/38tchqF4TIpLcTB07Mq2VN7sr7m\nmhUCAwEAAaNgMF4wHwYDVR0jBBgwFoAUCMCTC625/pgYnW3XnDA258o8vaYwHQYD\nVR0OBBYEFGanigGWdRibM+4AV04P8gVscQ7+MAwGA1UdEwEB/wQCMAAwDgYDVR0P\nAQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQCZjBM1FIB2xRKLgryaJwDiX93k\nVdwGDgITd4AsHpyt0Ea1OEdSL7gkUFEI11tAn++1uMZ07HQ97qHYhwRYJBVc0v0R\n9hZZW8u89lqFOBT+w6/825w6vEI0uWvPdZtL4YOTWcXfDhMDotiNvqb0UUN/E+OG\n2d4FBeHqK+SWvv46xVhAxE8BkuoJG2Jwt8VrWlHC2PC2joHN1D2bYrKJgpwTlYSP\nxsM5Rqxjy91Zipw8Upsy4Zwv5mx6HHx8JF/T4C8wwSuOzRsdoKTjFL5w5NuFQygA\naxiU3BcGcCDMZV5TY4Mdy5txeiJkqwnFIxHKHwq62BPbO+94CuWEEB/M/WYk\n-----END CERTIFICATE-----\n",
    "keyPair": {
        "PublicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA71IUYBMqSoXHtvhkaO60\nmULHeRcANgWOkl4JL71IRXPq32ihb9WgbKWacuNjoiP0u2Qnu5RRCBqFoVAKSD0+\nDmhux7/WwRwlkgroCLLnDJIJVDMXMoAGRBJ/aBvfL07+IhCaPWINcjbMTB6XjArd\n3pvCIHdTjTYgH7thsEnRq2WYk4zkb++FnbV8MTL7em6s1wo7+TIYkeBqe2GRcplR\nKrCC/c0Xx4uR2x8J2g0gfSbvbTzSItyscI43js42/6100E5F5GINqJfHXyvs4wCm\nwcwfu6xX8OxGw9T1VS9C1LID+hiRYJnmYtr/fy1yGoXhMiktxMHTsyrZU3uyvuaa\nFQIDAQAB\n-----END PUBLIC KEY-----\n",
        "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA71IUYBMqSoXHtvhkaO60mULHeRcANgWOkl4JL71IRXPq32ih\nb9WgbKWacuNjoiP0u2Qnu5RRCBqFoVAKSD0+Dmhux7/WwRwlkgroCLLnDJIJVDMX\nMoAGRBJ/aBvfL07+IhCaPWINcjbMTB6XjArd3pvCIHdTjTYgH7thsEnRq2WYk4zk\nb++FnbV8MTL7em6s1wo7+TIYkeBqe2GRcplRKrCC/c0Xx4uR2x8J2g0gfSbvbTzS\nItyscI43js42/6100E5F5GINqJfHXyvs4wCmwcwfu6xX8OxGw9T1VS9C1LID+hiR\nYJnmYtr/fy1yGoXhMiktxMHTsyrZU3uyvuaaFQIDAQABAoIBAQDWZdoLGCBTEvaQ\nXIbX2sHAa6r4ODrgKqpHRidEtXYBgo9wBfRalC9cJh/vvPaNU1j0aA2QZpcRg3Ej\nyujrPrJRhg14tcxWxDiEVXD6GgwTnuDspbiqbTcv1MJ/KjkP0Nyq9+S2CRmysJTl\nvKJXu4R44WFQZJZdc5fj1aL2o6tKt8YwG4txwPjUX3FpRPKRmDWQT5mZ+GADpUSY\nX93LFPaoWnVKJBWFmzyYlwUlMZA5KSV3Wuh95dG2IEXB/mvOyhB7wEYeZgCLnogS\nAyx5MnsS37bz+6tfkjEuHW0OPcbbxEgk6KWRJIF4EONgvvcYzjXQKaaLzJzOaQAG\nwYNN4foBAoGBAPkY2oTrGibDbA25psHHTFM4BfCdYz8avFdk8xrc5Vp2thnahNoD\nJNCtCE4PSNYfUmo1x9+HijNorqsYLp/mJ9Zp7IpmmrwyzU2oS7Kmg3aTmQK6FW3K\nJaeisyQj/KtC3gBt9fskvmRcYH7jMcfgYoJO0i12iuGVqUCsfo46cuzxAoGBAPXz\n3qhvL/K6yX5V0uoswY5KeY9NW7HkOq1YwgOQxcfnJTiqnm++9NrWK4h/N7oMGGgx\nR/NNBOWIKTzaOoLqRBQRIGPWmvzUOIwhN6YSopAwCUgaumSA/d8jBZVsT3y0I3VT\n5tKtQA/NHzxWfNWNPTluhZv+4P5YgGHagMdifQ9lAoGAKxkUvciblrdbG6jSZFai\nKwfXZ0Ej6cgrbAeIVE6B1DwT17dKIxpGJWC6vh7A4GM89Cln8pHV5H0pM2sUrg+5\nNszO40dLYGJ9yQDkT/2lYz+4SpN9n6hJCY8J5afgUJVaKcLcu14pHt4ox+txMn7t\nLFSM4tbOwqcNSKZPozYTqlECgYEAy3ZloILycGMy4o8O/uftas+TRgfhrgS2wcYm\nIZr28or10K3ciWa32fzIYI+VQxRUcIUsF0qEnXkJXCzPsJMppEwStmTHLBZHfSzR\ng1HxJ0SFuR9bSF8pJRksulKyYuAGYT36OhhWYXv3tgt6E5NWrZcPcl/kMqR19/0x\nAUApYr0CgYEA3axsg1mXKqs29dYCwQyFmOQQcJZ/fYq5CfIxzwi8vO0y1mQUY/1P\nHWmaO2HcFmiOcFPyOPmc+6lwiDsVq2L2menmiY6V9x5s8W9bYjvXqpgoP4QUxABC\nXK99geols6k9EtrfzHI6AV2o1Fd+Jw35ieLnve17kdfi0NnNcQfz7Ng=\n-----END RSA PRIVATE KEY-----\n"
    }
}

def get_credentials(iot_keys_and_certificates, iot_credential_endpoint, aws_cert_url):
    cert = tempfile.NamedTemporaryFile(delete=False)
    key = tempfile.NamedTemporaryFile(delete=False)
    cacert = tempfile.NamedTemporaryFile(delete=False)
    cert.write(iot_keys_and_certificates["certificatePem"].encode())
    cert.close()
    key.write(iot_keys_and_certificates["keyPair"]["PrivateKey"].encode())
    key.close()
    cacert.write(requests.get(aws_cert_url).text.encode())
    cacert.close()
    cert_and_key = (cert.name, key.name)  
    response = requests.get(iot_credential_endpoint, cert=cert_and_key,  verify=cacert.name)
    return response.json()



# iot_credential_endpoint = "https://c2qoqgl91j3vzz.credentials.iot.eu-central-1.amazonaws.com/role-aliases/kvs_iamrole_alias_a0e5c2f/credentials"
iot_credential_endpoint = "https://c2qoqgl91j3vzz.credentials.iot.eu-central-1.amazonaws.com/role-aliases/kvs_iamrole_alias_466f401/credentials"
aws_cert_url = b"https://www.amazontrust.com/repository/SFSRootCAG2.pem"
creds = get_credentials(certificates_what, iot_credential_endpoint,aws_cert_url)


