#!/usr/bin/python3

import argparse
import requests
import os
import json


def verbose(message):
    if args.verbose:
        print(message)


def validate_url():
    if args.url:
        verbose("checking server reachable " + args.url)
        try:
            r = requests.get(args.url + "/api/")
            if r.status_code==200:
                verbose("server api is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + args.url)
            exit(1)
        try:
            f = open(saved_url_file, "w")
            f.write(args.url)
            f.close()
        except:
            verbose("error saving url to " + saved_url_file)
        return args.url
    else:
        verbose("no url given, checking for a saved one in " + saved_url_file)
        try:
            f = open(saved_url_file, "r")
            url = f.read()
        except:
            verbose("error finding saved url file - please provide a url with the -u option")
            exit(1)
        try:
            r = requests.get(url + "/api/")
            if r.status_code==200:
                verbose(url + " server api is ok " + str(r.status_code))
                return url
            else:
                verbose(url + " some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + url)
            exit(1)


def validate_key():
    if args.key:
        verbose("checking apikey " + args.key)
        try:
            headers = {'content-type': 'application/json', 'Authorization': 'Token ' + args.key}
            r = requests.get(url + "/api/v1/asset/", headers=headers)
            if r.status_code == 200:
                verbose("api key is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + args.key)
            exit(1)
        try:
            f = open(saved_api_file, "w")
            f.write(args.key)
            f.close()
        except:
            verbose("error saving apikey to " + saved_api_file)
        return args.key
    else:
        verbose("no apikey given, checking for a saved one in " + saved_api_file)
        try:
            f = open(saved_api_file, "r")
            key = f.read()
        except:
            verbose("error finding saved api file - please provide a api with the -a option")
            exit(1)
        try:
            headers = {'content-type': 'application/json', 'Authorization': 'Token ' + key}
            r = requests.get(url + "/api/v1/asset/", headers=headers)
            if r.status_code == 200:
                verbose("api key is ok " + str(r.status_code))
            else:
                verbose("some server issue " + str(r.status_code))
                exit(1)
        except:
            verbose("error connecting to server " + url)
            exit(1)
        return key


def search_org():
    verbose("searching for org " + args.org)
    name = "name_like"
    if args.exact:
        name = "name"

    try:
        r = requests.get(url + "/api/v1/org/?" + name + "=" + args.org, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


def add_org():
    verbose("adding org " + args.org)
    try:
        data = '{"name":"' + args.org + '","comment": "' + args.comment + '","sector": "' + args.sector + '","level": "' + args.level + '","tier": ' + str(args.tier) + '}'
        verbose(data)
        r = requests.post(url + "/api/v1/org/", data, headers=headers)
        if r.status_code == 201:
            print(str(r.text))
        elif r.status_code == 400:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def delete_org_by_id(org_id):
    verbose("deleting org by id " + org_id)

    verbose("checking if the org has any assets")
    try:
        r = requests.get(url + "/api/v1/asset/?org_id=" + org_id, headers=headers)
        if r.status_code == 200:
            assets = json.loads(r.text)
            if assets:
                verbose("the org has some assets")
                if args.override:
                    verbose("override is set, lets delete some assets")
                    for asset in assets:
                        verbose("deleting " + str(asset["id"]))
                        delete_asset(str(asset["id"]))
                else:
                    print('{"detail": "the org has existing assets, not deleting anything, use --override or -o if you want to also delete the assets"}')
                    return
            else:
                verbose("the org has no assets, safe to delete")
        else:
            verbose("some server issue " + str(r.status_code))
            return
    except:
        verbose("error connecting to server " + url + " with key " + key)
        return

    verbose("made it to here, we either deleted the assets or there were none")
    try:
        r = requests.delete(url + "/api/v1/org/" + org_id + "/", headers=headers)
        if r.status_code == 204:
            print('{"detail":"delete org id ' + org_id + ' successful"})')
        elif r.status_code == 404:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)

def delete_org_by_name(org_name):
    verbose("deleting org by name " + org_name)

    try:
        r = requests.get(url + "/api/v1/org/?name=" + org_name, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                org_id = str((result[0]["id"]))
                delete_org_by_id(org_id)
            else:
                print('{"detail":"org name ' + org_name + ' not found"})')
    except:
        verbose("error connecting to server " + url + " with key " + key)


def delete_org():
    if args.org.isnumeric():
        delete_org_by_id(args.org)
    else:
        delete_org_by_name(args.org)


def modify_org():
    verbose("modifying org " + args.org)

    # first get the id
    try:
        r = requests.get(url + "/api/v1/org/?name=" + args.org, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                org_id = str((result[0]["id"]))
            else:
                print('{"detail":"org name ' + args.org + ' not found"})')
                return
    except:
        verbose("error connecting to server " + url + " with key " + key)

    # next modify it
    try:
        data = '{"name":"' + args.org + '","comment": "' + args.comment + '","sector": "' + args.sector + '","level": "' + args.level + '","tier": ' + str(args.tier) + '}'

        r = requests.put(url + "/api/v1/org/" + org_id + "/", data, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def search_asset():
    verbose("searching for asset " + args.asset)
    name = "name_like"
    if args.exact:
        name = "name"

    try:
        r = requests.get(url + "/api/v1/asset/?" + name + "=" + args.asset, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


def add_asset():
    verbose("adding asset " + args.asset + " to org " + args.org_name)

    verbose("first lets get the org id from the org name")
    try:
        r = requests.get(url + "/api/v1/org/?name=" + args.org_name, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                org_id = (result[0]["id"])
            else:
                verbose("could not find org " + args.org_name)
                return
        else:
            verbose("some server issue " + str(r.status_code))
            return
    except:
        verbose("error getting org id")

    try:
        data = '{"name":"' + args.asset + '","org":' + str(org_id) + ',"type": "' + args.asset_type + '","comment":"' + args.comment + '"}'
        verbose(data)
        r = requests.post(url + "/api/v1/asset/", data, headers=headers)
        if r.status_code == 201:
            print(str(r.text))
        elif r.status_code == 400:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)


def delete_asset(asset):
    if asset.isnumeric():
        delete_asset_by_id(asset)
    else:
        delete_asset_by_name(asset)


def delete_asset_by_id(asset_id):
    verbose("deleting asset by id " + asset_id)

    try:
        r = requests.delete(url + "/api/v1/asset/" + asset_id + "/", headers=headers)
        if r.status_code == 204:
            print('{"detail":"delete asset id ' + asset_id + ' successful"})')
        elif r.status_code == 404:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error deleting asset by id " + asset_id)


def delete_asset_by_name(asset_name):
    verbose("deleting asset by name " + asset_name)

    try:
        r = requests.get(url + "/api/v1/asset/?name=" + asset_name, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                asset_id = str((result[0]["id"]))
                delete_asset_by_id(asset_id)
            else:
                verbose("could not find asset " + asset_name)
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error getting org id")


def modify_asset():
    verbose("modifying asset " + args.asset)

    # first get the ids
    try:
        r = requests.get(url + "/api/v1/asset/?name=" + args.asset, headers=headers)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result:
                asset_id = str((result[0]["id"]))
                org_id = str((result[0]["org"]))
            else:
                print('{"detail":"asset name ' + args.asset + ' not found"})')
                return
    except:
        verbose("error connecting to server " + url + " with key " + key)

    # next modify it
    try:
        data = '{"name":"' + args.asset + '","org":"' + org_id + '","type": "' + args.asset_type + '","comment":"' + args.comment + '"}'

        r = requests.patch(url + "/api/v1/asset/" + asset_id + "/", data, headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key + " and data " + data)

def dump_all():
    verbose("dumping everything")

    try:
        r = requests.get(url + "/api/v1/org/", headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)

    try:
        r = requests.get(url + "/api/v1/asset/", headers=headers)
        if r.status_code == 200:
            print(str(r.text))
        else:
            verbose("some server issue " + str(r.status_code))
    except:
        verbose("error connecting to server " + url + " with key " + key)


if __name__ == "__main__":
    saved_url_file = os.environ['HOME'] + "/.assma.url"
    saved_api_file = os.environ['HOME'] + "/.assma.api"

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-u", "--url", metavar='', help="assma url eg. http://127.0.0.1:8000 or https://assma.mysite.com or saved in ~.assma.url")
    parser.add_argument("-k", "--key", metavar='', help="your 40 char apikey - or saved in ~.assma.api")
    parser.add_argument("-c", "--comment", metavar='', help="a comment", default="")
    parser.add_argument("-n", "--org_name", metavar='', help="the org to use when adding a asset")
    parser.add_argument("--sector", metavar='', help="the sector the org belongs to")
    parser.add_argument("--level", metavar='', help="National, Emirate")
    parser.add_argument("--tier", metavar='', help="Tier number of the org - 1 - 5")
    parser.add_argument("--asset_type", metavar='', help="domain, ipv4, range4, netmask4, cidr4, ipv6, range6, cidr6")
    parser.add_argument("-o", "--override", help="by default you can't delete orgs that have assets, override will also delete all assets, then the org", action="store_true")
    parser.add_argument("-e", "--exact", help="by default searching does partial matches, use this flag if you want exact match", action="store_true")

    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("-a", "--add", help="add asset or org", action="store_true")
    operation.add_argument("-d", "--delete", help="delete a asset or org", action="store_true")
    operation.add_argument("-m", "--modify", help="modify a asset or org", action="store_true")
    operation.add_argument("-s", "--search", help="search a asset or org", action="store_true")

    table = parser.add_mutually_exclusive_group()
    table.add_argument("--org", metavar='', help="operate on organisations")
    table.add_argument("--asset", metavar='', help="operate on assets")
    table.add_argument("--dump", help="dump all data, orgs first then assets", action="store_true")

    args = parser.parse_args()

    url = validate_url()
    key = validate_key()

    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + key}

    if args.dump:
        dump_all()

    if args.org:
        if args.search:
            search_org()
        if args.add:
            add_org()
        if args.delete:
            delete_org()
        if args.modify:
            modify_org()


    if args.asset:
        if args.search:
            search_asset()
        if args.add:
            add_asset()
        if args.delete:
            # delete_asset needs to receive an arg because delete_org sends one
            delete_asset(args.asset)
        if args.modify:
            modify_asset()

