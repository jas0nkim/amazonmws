import shlex, subprocess


if __name__ == "__main__":

    command_line = "casperjs amazon_mobile.js --root_path='/Users/jasonkim/Sites/amazonmws' --user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4' --asin='B0012OPLIE' --amazon_user='redflagitems.0020@gmail.com' --amazon_pass='12ReDF002AZIt!em!s' --buyer_name='Steven Schlusselberg' --buyer_addr_1='28 Windsor Rd' --buyer_addr_2=' ' --buyer_city='Great Neck' --buyer_state='NY' --buyer_zip='11021-2708' --buyer_phone='5162368947'"
    

    # p = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # args = [
    #     'casperjs',
    #     'amazon_mobile.js',
    #     "--root_path=/Users/jasonkim/Sites/amazonmws",
    #     "--user_agent=Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4",
    #     "--asin=B0012OPLIE",
    #     "--amazon_user=redflagitems.0020@gmail.com",
    #     "--amazon_pass=12ReDF002AZIt!em!s",
    #     "--buyer_name=Steven Schlusselberg",
    #     "--buyer_addr_1=28 Windsor Rd",
    #     "--buyer_addr_2= ",
    #     "--buyer_city=Great Neck",
    #     "--buyer_state=NY",
    #     "--buyer_zip=11021-2708",
    #     "--buyer_phone=5162368947",
    # ]

    args = shlex.split(command_line)

    print args

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p.wait()
    
    for line in p.stdout:
        print line
