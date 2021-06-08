# k8s-mobilenetworks

This repository is designed for learning purposes only.

## Download

```bash
$ git clone https://github.com/mobile-core/k8s-mobilenetworks.git
```

## Deploy

Deployment order

> NRF > UDR > UDM > AUSF > NSSF > AMF > PCF > UPF > SMF > N3IWF

```bash
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-mongodb
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-nrf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-udr
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-udm
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-ausf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-nssf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-amf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-pcf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-upf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-smf
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-webui
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-gnb
$ kubectl apply -k ~/k8s-mobilenetworks/manifests/f5gc-ue
```

## Delete

```bash
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-mongodb
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-nrf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-udr
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-udm
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-ausf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-nssf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-amf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-pcf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-upf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-smf
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-webui
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-gnb
$ kubectl delete -k ~/k8s-mobilenetworks/manifests/f5gc-ue
```

## Test

### Registration and PDU Session Establishment

```bash
$ kubectl exec -n f5gc -it [ue uuid] -c f5gc-ue -- /bin/bash
root@f5gc-ue-77dbf848bf-w6kh2# ./build/nr-ue -c ./config/free5gc-ue.yaml
```

### PDU Session Release

```bash
root@f5gc-ue-77dbf848bf-w6kh2# ./build/nr-cli imsi-208930000000003 --exec "ps-release [session number]"
```

### De-Registration

```bash
root@f5gc-ue-77dbf848bf-w6kh2# ./build/nr-cli imsi-208930000000003 --exec "deregister switch-off"
```

## NOTE

Currently, it is not possible to flow the user plane after attaching.

## Reference

- [Free5GC](https://github.com/free5gc/free5gc.git)
- [UERANSIM](https://github.com/aligungr/UERANSIM)
- [Open5GS](https://github.com/open5gs/open5gs)
