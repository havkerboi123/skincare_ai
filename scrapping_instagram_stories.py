import instaloader 
loader = instaloader.Instaloader(dirname_pattern="/Users/mhmh/Desktop/p2/skincare/{target}")
loader.login('', ')   
profile = instaloader.Profile.from_username(loader.context, 'organic_traveller')
loader.download_highlights(profile)
