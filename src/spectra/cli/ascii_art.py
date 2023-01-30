from spectra import version


def get_logo(
    star_color, star_color2, star_color3, 
    special_color1, special_color2, 
    info_color, logo_color
    ):
    art = f'''
  [{star_color2}].[/{star_color2}]  [{star_color3}]'[/{star_color3}]  [{star_color}]*[/{star_color}]   [{special_color1}].[/{special_color1}]  [{star_color2}].[/{star_color2}] [{star_color3}]'[/{star_color3}]     [{logo_color}]__                 _[/{logo_color}]            
    [{star_color2}].[/{star_color2}]  [{star_color}]*[/{star_color}] [{star_color}]*[/{star_color}] [{special_color1}]-[{special_color2}]+[/{special_color2}]-[/{special_color1}]        [{logo_color}]/ _\_ __   ___  ___| |_ _ __ __ _[/{logo_color}]
[{star_color2}].[/{star_color2}]    [{star_color}]*[/{star_color}] [{star_color2}].[/{star_color2}]    [{special_color1}]'[/{special_color1}]  [{star_color}]*[/{star_color}]      [{logo_color}]\ \| '_ \ / _ \/ __| __| '__/ _` |[/{logo_color}]
    [{star_color}]*[/{star_color}] [{star_color2}].[/{star_color2}]  [{star_color3}]'[/{star_color3}] [{star_color2}].[/{star_color2}]  [{star_color2}].[/{star_color2}]       [{logo_color}]_\ \ |_) |  __/ (__| |_| | | (_| |[/{logo_color}]
 [{star_color}]*[/{star_color}]   [{star_color}]*[/{star_color}]  [{star_color2}].[/{star_color2}]   [{star_color2}].[/{star_color2}]         [{logo_color}]\__/ .__/ \___|\___|\__|_|  \__,_|[/{logo_color}]
    [{star_color3}]'[/{star_color3}]   [{star_color}]*[/{star_color}]                [{logo_color}]|_|[/{logo_color}] [{info_color}]v{version}, © 2023, Josh Kaplan[/{info_color}]             
'''
    return art