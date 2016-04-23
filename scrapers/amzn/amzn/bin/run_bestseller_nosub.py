import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls=[
        # Industrial & Scientific - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial',

        # Abrasive & Finishing Products - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Products/zgbs/industrial/256167011',

        # Abrasive Accessories - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Accessories/zgbs/industrial/401506011',

        # Abrasive Dressing Tools - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Dressing-Tools/zgbs/industrial/256180011',

        # Abrasive Mandrels - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Mandrels/zgbs/industrial/401510011',

        # Abrasive Wheel Adapters & Flanges - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheel-Adapters-Flanges/zgbs/industrial/2734041011',

        # Tool Holders - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tool-Holders/zgbs/industrial/401549011',

        # Industrial Sander Belts - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sander-Belts/zgbs/industrial/3442587011',

        # Abrasive Brushes - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Brushes/zgbs/industrial/256168011',

        # Power Sander Bristle Discs - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Bristle-Discs/zgbs/industrial/310357011',

        # Abrasive Power Brushes - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Power-Brushes/zgbs/industrial/2665577011',

        # Abrasive Cup Power Brushes - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cup-Power-Brushes/zgbs/industrial/2665578011',

        # Abrasive Flat End Power Brushes - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Flat-End-Power-Brushes/zgbs/industrial/2665579011',

        # Abrasive Spiral Power Brushes - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Spiral-Power-Brushes/zgbs/industrial/2665580011',

        # Abrasive Wheel Power Brushes - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheel-Power-Brushes/zgbs/industrial/2665581011',

        # Scratch Brushes - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Scratch-Brushes/zgbs/industrial/1265107011',

        # Abrasive Mounted Points - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Mounted-Points/zgbs/industrial/401518011',

        # Abrasive Bands - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Bands/zgbs/industrial/401505011',

        # Abrasive Cartridge Rolls - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cartridge-Rolls/zgbs/industrial/256169011',

        # Power Sanding Sleeves - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sanding-Sleeves/zgbs/industrial/552596',

        # Abrasive Grinding Cones & Plugs - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Cones-Plugs/zgbs/industrial/2734046011',

        # Abrasive Grinding Mounted Points - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Mounted-Points/zgbs/industrial/2734045011',

        # Abrasive Wheels & Discs - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheels-Discs/zgbs/industrial/2665570011',

        # Angle & Die Grinder Wheels - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Angle-Die-Grinder-Wheels/zgbs/industrial/2665571011',

        # Bench & Pedestal Grinding Wheels - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bench-Pedestal-Grinding-Wheels/zgbs/industrial/256204011',

        # Abrasive Cutoff Wheels - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cutoff-Wheels/zgbs/industrial/256194011',

        # Power Sander Flap Discs - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Flap-Discs/zgbs/industrial/256175011',

        # Abrasive Flap Wheels - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Flap-Wheels/zgbs/industrial/256200011',

        # Abrasive Grinding Discs - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Discs/zgbs/industrial/2665574011',

        # Abrasive OD Grinding Wheels - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-OD-Grinding-Wheels/zgbs/industrial/2665575011',

        # Power Oscillating Tool Sanding Pads - 15
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Oscillating-Tool-Sanding-Pads/zgbs/industrial/8106528011',

        # Abrasive Sanding Disc Backing Pads - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Sanding-Disc-Backing-Pads/zgbs/industrial/2665576011',

        # Power Sanding Discs - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sanding-Discs/zgbs/industrial/552588',

        # Power Sander Fiber Backed Abrasive Discs - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Fiber-Backed-Abrasive-Discs/zgbs/industrial/256176011',

        # Power Sander Hook & Loop Discs - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Hook-Loop-Discs/zgbs/industrial/256177011',

        # Power Sander PSA Discs - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-PSA-Discs/zgbs/industrial/256178011',

        # Power Sander Quick Change Discs - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Quick-Change-Discs/zgbs/industrial/256179011',

        # Surface Grinding Wheels - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Surface-Grinding-Wheels/zgbs/industrial/256207011',

        # Abrasive Tool Room Grinding Wheels - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Tool-Room-Grinding-Wheels/zgbs/industrial/256202011',

        # Unitized & Convolute Wheels - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Unitized-Convolute-Wheels/zgbs/industrial/256203011',

        # Abrasive Finishing Products - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Products/zgbs/industrial/2734049011'

        # Buffing & Polishing Accessories - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Polishing-Accessories/zgbs/industrial/256209011',

        # Buffing & Polishing Mounted Points - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Polishing-Mounted-Points/zgbs/industrial/979146011',

        # Buffing Kits - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Kits/zgbs/industrial/256211011',

        # Buffing Wheels - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Wheels/zgbs/industrial/256214011',

        # Felt Bobs - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Felt-Bobs/zgbs/industrial/256215011',

        # Abrasive Finishing Compounds - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Compounds/zgbs/industrial/2734050011',

        # Laps & Hones - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Laps-Hones/zgbs/industrial/256182011',

        # Flex Hones - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flex-Hones/zgbs/industrial/256184011',

        # Honing Stones - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Honing-Stones/zgbs/industrial/256185011',

        # Tumbling Media - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tumbling-Media/zgbs/industrial/256192011',

        # Hand Files - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Files/zgbs/industrial/256181011',

        # Manual Sanding Products - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Manual-Sanding-Products/zgbs/industrial/2734051011',

        # Sanding Blocks - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Blocks/zgbs/industrial/553332',

        # Sanding Pads - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Pads/zgbs/industrial/2734054011',

        # Sanding Rolls - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Rolls/zgbs/industrial/401511011',

        # Sanding Sheets - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Sheets/zgbs/industrial/256189011',

        # Sanding Sponges - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Sponges/zgbs/industrial/2734053011',

        # Sanding Tapes - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Tapes/zgbs/industrial/401512011',

        # Sanding Steel Wool - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Steel-Wool/zgbs/industrial/2734052011',

        # Power Sand Blasters - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sand-Blasters/zgbs/industrial/552714',

        # Sharpening Stones - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sharpening-Stones/zgbs/industrial/553346',

        # Additive Manufacturing Products - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Additive-Manufacturing-Products/zgbs/industrial/6066126011',

        # 3D Printers - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printers/zgbs/industrial/6066127011',

        # 3D Printing Supplies - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printing-Supplies/zgbs/industrial/6066128011',

        # 3D Printer Parts & Accessories - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Parts-Accessories/zgbs/industrial/6066132011',

        # 3D Printer Extruders - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Extruders/zgbs/industrial/8481415011',

        # 3D Printer Platforms - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Platforms/zgbs/industrial/8481418011',

        # 3D Printer Motors - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Motors/zgbs/industrial/8481417011',

        # 3D Printer Interface & Driver Modules - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Interface-Driver-Modules/zgbs/industrial/8481416011',

        # 3D Printer Controllers - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Controllers/zgbs/industrial/8481414011',

        # 3D Printer Accessories - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Accessories/zgbs/industrial/8481419011',

        # Commercial Door Products - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Products/zgbs/industrial/10773802011',

        # Commercial Access Control - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Control/zgbs/industrial/10773803011',

        # Commercial Access Cards & Card Readers - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Cards-Card-Readers/zgbs/industrial/10773804011',

        # Commercial Door Control - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Control/zgbs/industrial/10773848011',

        # Commercial Access Door Control - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Door-Control/zgbs/industrial/10773853011',

        # Security Access-Control Keypads - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Security-Access-Control-Keypads/zgbs/industrial/11041131',

        # Commercial Electromagnetic Locks - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Electromagnetic-Locks/zgbs/industrial/10773876011',

        # Commercial Door Hardware - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Hardware/zgbs/industrial/10773891011',

        # Commercial Door Guards - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Guards/zgbs/industrial/10773913011',

        # Commercial Door Hinges - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Hinges/zgbs/industrial/10773915011',

        # Commercial Door Stops - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Stops/zgbs/industrial/10773917011',

        # Commercial Exit Devices - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Exit-Devices/zgbs/industrial/10773918011',

        # Commercial Push & Pull Locksets & Handles - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Push-Pull-Locksets-Handles/zgbs/industrial/10773952011',

        # Sliding Door Hardware - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sliding-Door-Hardware/zgbs/industrial/9628854011',

        # Cutting Tools - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Tools/zgbs/industrial/383598011',

        # Band Saw Blades - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Band-Saw-Blades/zgbs/industrial/552288',

        # Broaches - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Broaches/zgbs/industrial/340030011',

        # Cutting Burs - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Burs/zgbs/industrial/256263011',

        # Cutting Tool Coolants - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Tool-Coolants/zgbs/industrial/401548011',

        # Deburring Cutters - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Deburring-Cutters/zgbs/industrial/340035011',

        # Drill & Tap Sets - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drill-Tap-Sets/zgbs/industrial/8906585011',

        # Hole Saws & Accessories - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saws-Accessories/zgbs/industrial/552402',

        # Hole Saw Arbors - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saw-Arbors/zgbs/industrial/8106327011',

        # Hole Saw Sets & Kits - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saw-Sets-Kits/zgbs/industrial/8106328011',

        # Hole Saws - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saws/zgbs/industrial/256292011',

        # Indexable Insert Holders - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Insert-Holders/zgbs/industrial/257513011',

        # Drilling Holders - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drilling-Holders/zgbs/industrial/257515011',

        # Face Mill Holders - 1
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Face-Mill-Holders/zgbs/industrial/262582011',

        # Indexable Inserts - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Inserts/zgbs/industrial/257519011',

        # Turning Inserts - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Turning-Inserts/zgbs/industrial/257522011',

        # Industrial Drill Bits - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drill-Bits/zgbs/industrial/256264011',

        # Combination Drill & Taps - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Combination-Drill-Taps/zgbs/industrial/6001488011',

        # Masonry Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Masonry-Drill-Bits/zgbs/industrial/256276011',

        # Core Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Core-Drill-Bits/zgbs/industrial/256268011',

        # Masonry Drill Bit Sets - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Masonry-Drill-Bit-Sets/zgbs/industrial/8906589011',

        # Rotary Hammer Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rotary-Hammer-Drill-Bits/zgbs/industrial/8906591011',

        # Metalworking & Multipurpose Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Metalworking-Multipurpose-Drill-Bits/zgbs/industrial/2941336011',

        # Annular Cutters - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Annular-Cutters/zgbs/industrial/340028011',

        # Circuit Board Drill Bits - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Circuit-Board-Drill-Bits/zgbs/industrial/401551011',

        # Industrial Indexable Inserts - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Inserts/zgbs/industrial/8906583011',

        # Metalworking & Multipurpose Drill Sets - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Metalworking-Multipurpose-Drill-Sets/zgbs/industrial/8906587011',

        # Reduced Shank Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Reduced-Shank-Drill-Bits/zgbs/industrial/340052011',

        # Step Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Step-Drill-Bits/zgbs/industrial/256287011',

        # Subland Drill Bits - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Subland-Drill-Bits/zgbs/industrial/2941338011',

        # Twist Drill Bits - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Twist-Drill-Bits/zgbs/industrial/552416',

        # Extra Long Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Extra-Long-Drill-Bits/zgbs/industrial/256270011',

        # Hex-Shank Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Shank-Drill-Bits/zgbs/industrial/552400',

        # Jobber Drill Bits - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Jobber-Drill-Bits/zgbs/industrial/256275011',

        # Long Length Drill Bits - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Long-Length-Drill-Bits/zgbs/industrial/256289011',

        # Mechanic's Length Drill Bits - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Mechanics-Length-Drill-Bits/zgbs/industrial/2941341011',

        # Short Length Drill Bits - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Short-Length-Drill-Bits/zgbs/industrial/2941342011',

        # Wood Drill Bit Sets - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wood-Drill-Bit-Sets/zgbs/industrial/8906593011',

        # Wood Drill Bits - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wood-Drill-Bits/zgbs/industrial/256291011',

        # Auger Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Auger-Drill-Bits/zgbs/industrial/552410',

        # Boring Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Boring-Drill-Bits/zgbs/industrial/552392',

        # Brad-Point Drill Bits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Brad-Point-Drill-Bits/zgbs/industrial/552394',

        # Forstner Drill Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Forstner-Drill-Bits/zgbs/industrial/552398',

        # Self-Feed Drill Bits - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Self-Feed-Drill-Bits/zgbs/industrial/552408',

        # Spade Drill Bits - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spade-Drill-Bits/zgbs/industrial/552412',

        # Countersink Drill Bits - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Countersink-Drill-Bits/zgbs/industrial/552396',

        # Milling Tools - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Milling-Tools/zgbs/industrial/5825198011',

        # End Mills - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-End-Mills/zgbs/industrial/256305011',

        # Ball Nose End Mills - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ball-Nose-End-Mills/zgbs/industrial/340044011',

        # Square Nose End Mills - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Square-Nose-End-Mills/zgbs/industrial/2382225011',

        # Tapered End Mills - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tapered-End-Mills/zgbs/industrial/340047011',

        # Hand Punches - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Punches/zgbs/industrial/2225051011',

        # Arch Punches - 15
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Arch-Punches/zgbs/industrial/2225054011',

        # Center Punches - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Center-Punches/zgbs/industrial/2225055011',

        # Drift Punches - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drift-Punches/zgbs/industrial/2225056011',

        # Hole Punches - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Punches/zgbs/industrial/2225057011',

        # Knockout Punches - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Knockout-Punches/zgbs/industrial/2225058011',

        # Pin Punches - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pin-Punches/zgbs/industrial/2225059011',

        # Transfer Punches - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Transfer-Punches/zgbs/industrial/2225060011',

        # Bridge & Construction Reamers - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bridge-Construction-Reamers/zgbs/industrial/2611570011',

        # Hand Reamers - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Reamers/zgbs/industrial/256298011',

        # Taper Pin Reamers - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Taper-Pin-Reamers/zgbs/industrial/256300011',

        # Taper Pipe Reamers - 2
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Taper-Pipe-Reamers/zgbs/industrial/2611571011',

        # Router Bits - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Bits/zgbs/industrial/3116511',

        # Router Bearings & Bit-Repair Parts - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Bearings-Bit-Repair-Parts/zgbs/industrial/3116521',

        # Router Door & Window Bits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Door-Window-Bits/zgbs/industrial/3116531',

        # Edge Treatment & Grooving Router Bits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Edge-Treatment-Grooving-Router-Bits/zgbs/industrial/3116541',

        # Joinery Router Bits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Joinery-Router-Bits/zgbs/industrial/3116551',

        # Solid Surface Router Bits - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solid-Surface-Router-Bits/zgbs/industrial/3116561',

        # Straight, Spiral & Trim Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Spiral-Trim-Bits/zgbs/industrial/3116571',

        # Spiral Router Bits - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spiral-Router-Bits/zgbs/industrial/686958011',

        # Straight Router Bits - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Router-Bits/zgbs/industrial/686957011',

        # Trim Router Bits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Trim-Router-Bits/zgbs/industrial/686959011',

        # Slotting Cutters - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slotting-Cutters/zgbs/industrial/256311011',

        # Slotting Cutter Arbors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slotting-Cutter-Arbors/zgbs/industrial/256313011',

        # Three Wing Slotting Cutters - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Three-Wing-Slotting-Cutters/zgbs/industrial/256314011',

        # Thread Repair Kits - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Repair-Kits/zgbs/industrial/15709071',

        # Thread Metric Inserts & Repair Kits - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Metric-Inserts-Repair-Kits/zgbs/industrial/15709091',

        # Thread Spark Plug Thread Repair Kits - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Spark-Plug-Repair-Kits/zgbs/industrial/15709101',

        # Threading Dies - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threading-Dies/zgbs/industrial/256320011',

        # Hex Threading Dies - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Threading-Dies/zgbs/industrial/256321011',

        # Round Threading Dies - 3
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Round-Threading-Dies/zgbs/industrial/256322011',

        # Threading Taps - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threading-Taps/zgbs/industrial/256324011',

        # Pipe Taps - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pipe-Taps/zgbs/industrial/340041011',

        # Straight Flute Taps - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Flute-Taps/zgbs/industrial/256326011',

        # Thread Milling Taps - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Milling-Taps/zgbs/industrial/340043011',




        # # Automotive Tools & Equipment - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Tools-Equipment/zgbs/automotive/15706941',

        # # Air Conditioning Tools & Equipment - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Conditioning-Tools-Equipment/zgbs/automotive/15706951',




        # # Automotive Paint & Paint Supplies - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Paint-Supplies/zgbs/automotive/13591416011',

        # # Body Repair Paint Spray Guns - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Body-Repair-Paint-Spray-Guns/zgbs/automotive/15707181',

        # # Automotive Performance Parts & Accessories - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Parts-Accessories/zgbs/automotive/15710351',

        # # Automotive Performance Batteries & Accessories - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Batteries-Accessories/zgbs/automotive/15710451',

        # # Automotive Performance Batteries - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Batteries/zgbs/automotive/15710461',

        # # Automotive Performance Battery Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Battery-Accessories/zgbs/automotive/15710471',

        # # Automotive Performance Climate Control Products - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Climate-Control-Products/zgbs/automotive/15711281',

        # # Automotive Performance Engine Cooling Systems - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Cooling-Systems/zgbs/automotive/15712301',

        # # Automotive Performance Engine Coolers & Accessories - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Coolers-Accessories/zgbs/automotive/15712321',

        # # Automotive Performance Engine Cooler Accessories - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Cooler-Accessories/zgbs/automotive/15712331',

        # # Automotive Performance Engine Oils - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Oils/zgbs/automotive/15712341',

        # # Automotive Performance Transmission Cooler Fluids - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Transmission-Cooler-Fluids/zgbs/automotive/15712351',

        # # Automotive Performance Engine Cooling & Climate Control - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Cooling-Climate-Control/zgbs/automotive/15712361',

        # # Automotive Performance Engine Fan Clutches - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Fan-Clutches/zgbs/automotive/15712371',

        # # Automotive Performance Engine Fan Electric Controls - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Fan-Electric-Controls/zgbs/automotive/15712411',

        # # Automotive Performance Engine Fans - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Fans/zgbs/automotive/15712421',

        # # Automotive Performance Rigid Engine Fans - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Rigid-Engine-Fans/zgbs/automotive/15712441',

        # # Automotive Performance Engine Fan Spacers - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Fan-Spacers/zgbs/automotive/15712481',

        # # Automotive Performance Thermostat Housings - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Thermostat-Housings/zgbs/automotive/15712521',

        # # Automotive Performance Thermostats - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Thermostats/zgbs/automotive/15712541',

        # # Automotive Performance Water Pump Fittings & Accessories - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Water-Pump-Fittings-Accessories/zgbs/automotive/15712551',

        # # Automotive Performance Water Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Water-Pumps/zgbs/automotive/15712561',

        # # Automotive Performance Engines & Engine Parts - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engines-Engine-Parts/zgbs/automotive/15712571',

        # # Automotive Performance Engine Blocks - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Blocks/zgbs/automotive/15713791',

        # # Automotive Performance Long Engine Blocks - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Long-Engine-Blocks/zgbs/automotive/15713801',

        # # Automotive Performance Short Engine Blocks - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Short-Engine-Blocks/zgbs/automotive/15713811',

        # # Automotive Performance Cam & Lifter Engine Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Cam-Lifter-Engine-Kits/zgbs/automotive/15712691',

        # # Automotive Performance Long Engine Block Kits - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Long-Engine-Block-Kits/zgbs/automotive/15712721',

        # # Automotive Performance Short Engine Block Kits - 1
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Short-Engine-Block-Kits/zgbs/automotive/15712811',

        # # Automotive Performance Engine Management Systems - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Management-Systems/zgbs/automotive/318338011',

        # # Automotive Performance Engine Parts - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Parts/zgbs/automotive/15712831',

        # # Automotive Performance Cam & Lifter Kits - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Cam-Lifter-Kits/zgbs/automotive/15712851'

        # # Automotive Performance Engine Cam Bearings - 1
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Cam-Bearings/zgbs/automotive/15712861',

        # # Automotive Performance Engine Camshafts & Parts - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Camshafts-Parts/zgbs/automotive/15712871',

        # # Automotive Performance Engine Camshaft Buttons - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Camshaft-Buttons/zgbs/automotive/15712881',

        # # Automotive Performance Connecting Engine Rods & Parts - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Connecting-Engine-Rods-Parts/zgbs/automotive/15712931',

        # # Automotive Performance Engine Connecting Rod Bearings - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Connecting-Rod-Bearings/zgbs/automotive/15712951',

        # # Automotive Performance Connecting Rod Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Connecting-Rod-Bolts/zgbs/automotive/15712961',

        # # Automotive Performance Crank Trigger Kits - 1
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Crank-Trigger-Kits/zgbs/automotive/15712981',

        # # Automotive Performance Engine Crankshaft Pulleys - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Crankshaft-Pulleys/zgbs/automotive/15712991',

        # # Automotive Performance Engine Crankshafts - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Crankshafts/zgbs/automotive/15713001',

        # # Automotive Performance Dipsticks - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Dipsticks/zgbs/automotive/15713021',

        # # Automotive Performance Engine Dowel Pins - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Dowel-Pins/zgbs/automotive/15713031',

        # # Automotive Performance Engine Mounts - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Mounts/zgbs/automotive/15713061',

        # # Automotive Performance Engine Expansion Plug Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Expansion-Plug-Kits/zgbs/automotive/15713081',

        # # Automotive Performance Engine Harmonic Balancer Repair Kits - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Harmonic-Balancer-Repair-Kits/zgbs/automotive/15713101',

        # # Automotive Performance Engine Harmonic Balancers - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Harmonic-Balancers/zgbs/automotive/15713111',

        # # Automotive Performance Engine Head Bolt Sets - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Head-Bolt-Sets/zgbs/automotive/15713121',

        # # Automotive Performance Intake Manifolds & Parts - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Intake-Manifolds-Parts/zgbs/automotive/15713131',

        # # Automotive Performance Engine Intake Manifold Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Intake-Manifold-Bolts/zgbs/automotive/15713141',

        # # Automotive Performance Engine Intake Manifold Spacers - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Intake-Manifold-Spacers/zgbs/automotive/15713151',

        # # Automotive Performance Engine Knurled Head Bolts - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Knurled-Head-Bolts/zgbs/automotive/15713161',

        # # Automotive Performance Engine Lifter Kits - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Lifter-Kits/zgbs/automotive/15713171',

        # # Automotive Performance Engine Main Bolts & Studs - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Main-Bolts-Studs/zgbs/automotive/15713201',

        # # Automotive Performance Engine Oil Drain Plugs - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Oil-Drain-Plugs/zgbs/automotive/15713221',

        # # Automotive Performance Engine Oil Pans - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Oil-Pans/zgbs/automotive/15713231',

        # # Automotive Performance Oil Pumps & Parts - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Oil-Pumps-Parts/zgbs/automotive/15713241',

        # # Automotive Performance High Pressure Oil Pumps - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-High-Pressure-Oil-Pumps/zgbs/automotive/15713251',

        # # Automotive Performance Oil Pump Primers & Drives - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Oil-Pump-Primers-Drives/zgbs/automotive/15713271',

        # # Automotive Performance Oil Pump Pushrods - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Oil-Pump-Pushrods/zgbs/automotive/15713281',

        # # Automotive Performance Oil Pump Repair Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Oil-Pump-Repair-Kits/zgbs/automotive/15713291',

        # # Automotive Performance Push Rod Guide Plates - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Push-Rod-Guide-Plates/zgbs/automotive/15713421',

        # # Automotive Performance Push Rod Tubes - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Push-Rod-Tubes/zgbs/automotive/15713431',

        # # Automotive Performance Push Rods - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Push-Rods/zgbs/automotive/15713441',

        # # Automotive Performance Rocker Arms & Parts - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Rocker-Arms-Parts/zgbs/automotive/15713451',

        # # Automotive Performance Rocker Arm Pivots - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Rocker-Arm-Pivots/zgbs/automotive/15713491',

        # # Automotive Performance Roller Rockers - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Roller-Rockers/zgbs/automotive/15713511',

        # # Automotive Performance Roto Caps & Spring Retainers - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Roto-Caps-Spring-Retainers/zgbs/automotive/15713521',

        # # Automotive Performance Timing Parts - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Timing-Parts/zgbs/automotive/15713541',

        # # Automotive Performance Timing Part Dampers - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Timing-Part-Dampers/zgbs/automotive/15713571',

        # # Automotive Performance Timing Part Sets & Kits - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Timing-Part-Sets-Kits/zgbs/automotive/15713621',

        # # Automotive Performance Torque Struts - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Torque-Struts/zgbs/automotive/15713631',

        # # Automotive Performance Turbocharger Boost Controllers - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbocharger-Boost-Controllers/zgbs/automotive/318365011',

        # # Automotive Performance Turbocharger Boost Gauges - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbocharger-Boost-Gauges/zgbs/automotive/318366011',

        # # Automotive Performance Turbocharger Hoses & Hose Clamps - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbocharger-Hoses-Hose-Clamps/zgbs/automotive/318372011',

        # # Automotive Performance Turbocharger Piping & Piping Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbocharger-Piping-Kits/zgbs/automotive/318369011',

        # # Automotive Performance Turbocharger Wastegates - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbocharger-Wastegates/zgbs/automotive/318376011',

        # # Automotive Performance Turbochargers - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Turbochargers/zgbs/automotive/15713641',

        # # Automotive Performance Engine Valve Covers - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Covers/zgbs/automotive/15713781',

        # # Automotive Performance Engine Valves & Parts - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valves-Parts/zgbs/automotive/15713651',

        # # Automotive Performance Engine Valve Adjusters - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Adjusters/zgbs/automotive/15713661',

        # # Automotive Performance Engine Valve Cover Bolts - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Cover-Bolts/zgbs/automotive/15713671',

        # # Automotive Performance Engine Valve Locks - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Locks/zgbs/automotive/15713711',

        # # Automotive Performance Engine Valve Seals - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Seals/zgbs/automotive/15713721',

        # # Automotive Performance Engine Valve Shims - 3
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Shims/zgbs/automotive/15713741',

        # # Automotive Performance Engine Valve Springs - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Valve-Springs/zgbs/automotive/15713751',

        # # Automotive Performance Exhaust Systems - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Systems/zgbs/automotive/15713821',

        # # Automotive Performance Catalytic Converters & Parts - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Catalytic-Converters-Parts/zgbs/automotive/15713831',

        # # Automotive Performance Catalytic Converters - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Catalytic-Converters/zgbs/automotive/15713841',

        # # Automotive Performance Exhaust Clamps - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Clamps/zgbs/automotive/15713911',

        # # Automotive Performance Complete Exhaust Kits - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Complete-Exhaust-Kits/zgbs/automotive/15713921',

        # # Automotive Performance Exhaust Coatings - 2
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Coatings/zgbs/automotive/15713931',

        # # Automotive Performance Exhaust Extension Pipes - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Extension-Pipes/zgbs/automotive/15713941',

        # # Automotive Performance Exhaust Flanges - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Flanges/zgbs/automotive/15713951',

        # # Automotive Performance Exhaust Hangers - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Hangers/zgbs/automotive/15713961',

        # # Automotive Performance Exhaust System Headers & Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-System-Headers-Accessories/zgbs/automotive/15713971',

        # # Automotive Performance Exhaust Header Bolts - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Header-Bolts/zgbs/automotive/15713981',

        # # Automotive Performance Exhaust Header Gaskets - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Header-Gaskets/zgbs/automotive/15713991',

        # # Automotive Performance Exhaust Headers - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Headers/zgbs/automotive/15873001',

        # # Automotive Performance Exhaust Heat Shields - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Heat-Shields/zgbs/automotive/15714011',

        # # Automotive Performance Exhaust Heat Wrap, Matting & Sleeving - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Heat-Wrap-Matting-Sleeving/zgbs/automotive/15714021',

        # # Automotive Performance Engine Intake Manifold & Parts - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Intake-Manifold-Parts/zgbs/automotive/15714031',

        # # Automotive Performance Engine Intake Manifold Bolt & Spring Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Engine-Intake-Manifold-Bolt-Spring-Kits/zgbs/automotive/15714041',

        # # Automotive Performance Exhaust Mufflers - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Mufflers/zgbs/automotive/15714071',

        # # Automotive Performance Exhaust Pipes - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Pipes/zgbs/automotive/15714081',

        # # Automotive Performance Exhaust Resonators - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Exhaust-Resonators/zgbs/automotive/15714121',

        # # Automotive Performance Filters - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Filters/zgbs/automotive/15714131',

        # # Automotive Performance Air Filters & Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Air-Filters-Accessories/zgbs/automotive/15714141',

        # # Automotive Performance Air Filters - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Air-Filters/zgbs/automotive/15714151',

        # # Air Filter Accessories & Cleaning Products - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Filter-Accessories-Cleaning-Products/zgbs/automotive/8606879011',

        # # Automotive Air Filter Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Filter-Accessories/zgbs/automotive/8606883011',

        # # Automotive Air Filter Cleaning Products - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Filter-Cleaning-Products/zgbs/automotive/8606881011',

        # # Automotive Performance Passenger Compartment Air Filters - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Performance-Passenger-Compartment-Air-Filters/zgbs/automotive/15714171',

        



        # # Oils & Fluids - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Oils-Fluids/zgbs/automotive/15718791',

        # # Oil & Fluid Additives - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Oil-Fluid-Additives/zgbs/automotive/15718801',

        # # Cooling System Additives - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cooling-System-Additives/zgbs/automotive/15718811'

        # # Engine & Oil Fluid Additives - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Engine-Oil-Fluid-Additives/zgbs/automotive/15718821',

        # # Fuel System Additives - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Fuel-System-Additives/zgbs/automotive/15718831',

        # # Diesel Additives - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Diesel-Additives/zgbs/automotive/15718841',

        # # Fuel Additives - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Fuel-Additives/zgbs/automotive/15718851',

        # # Octane Boosters - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Octane-Boosters/zgbs/automotive/15718861',

        # # Power Steering Fluid Additives - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Power-Steering-Fluid-Additives/zgbs/automotive/15718881',

        # # Transmission Fluid Additives - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Transmission-Fluid-Additives/zgbs/automotive/15718891',

        # # Antifreezes & Coolants - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Antifreezes-Coolants/zgbs/automotive/15718901',

        # # Body Repair & Restoration Chemicals - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Body-Repair-Restoration-Chemicals/zgbs/automotive/15718911',

        # # Body Repair & Restoration Adhesives - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Body-Repair-Restoration-Adhesives/zgbs/automotive/15718921',

        # # Automotive Paints & Primers - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Paints-Primers/zgbs/automotive/15709851',

        # # Automotive Body Paint - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Body-Paint/zgbs/automotive/15709861',

        # # Automotive Clear Coats - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Clear-Coats/zgbs/automotive/15709871',

        # # Automotive High Temperature Paint - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-High-Temperature-Paint/zgbs/automotive/15709891',

        # # Automotive Paint Removers - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Paint-Removers/zgbs/automotive/15709911',

        # # Automotive Primers - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Primers/zgbs/automotive/15709921',

        # # Automotive Spray Paint - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Spray-Paint/zgbs/automotive/15709941',

        # # Automotive Top Coats - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Top-Coats/zgbs/automotive/15709951',

        # # Automotive Touchup Paint - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Touchup-Paint/zgbs/automotive/15709961',

        # # Automotive Trim Dye - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Trim-Dye/zgbs/automotive/15709971',

        # # Automotive Undercoat Paint - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Undercoat-Paint/zgbs/automotive/15709981',

        # # Brake Fluids - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Brake-Fluids/zgbs/automotive/15718941',

        # # Engine & Parts Fluid Cleaners - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Engine-Parts-Fluid-Cleaners/zgbs/automotive/15718971',

        # # Brake Cleaners - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Brake-Cleaners/zgbs/automotive/15718981',

        # # Carburetor & Throttle Body Cleaners - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Carburetor-Throttle-Body-Cleaners/zgbs/automotive/15718991',

        # # Electrical Cleaners - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Electrical-Cleaners/zgbs/automotive/15719001',

        # # Engine Cleaners & Degreasers - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Engine-Cleaners-Degreasers/zgbs/automotive/15719011',

        # # Fuel System Cleaners - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Fuel-System-Cleaners/zgbs/automotive/15719031',

        # # Oil Cleanup Absorbers - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Oil-Cleanup-Absorbers/zgbs/automotive/15719071',

        # # Engine Part Cleaners - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Engine-Part-Cleaners/zgbs/automotive/15719081',

        # # Powersports Chemicals & Fluids - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Powersports-Chemicals-Fluids/zgbs/automotive/404702011',

        # # Flushes - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Flushes/zgbs/automotive/15719091',

        # # Engine Flushes - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Engine-Flushes/zgbs/automotive/15719111',

        # # Automotive Greases & Lubricants - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Greases-Lubricants/zgbs/automotive/15719191',

        # # Oils - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Oils/zgbs/automotive/15719331',

        # # Air Conditioning Oils - 5
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Conditioning-Oils/zgbs/automotive/15719341',

        # # Gear Oils - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Gear-Oils/zgbs/automotive/15719351',

        # # Hydraulic Oils - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Hydraulic-Oils/zgbs/automotive/15719381',

        # # Motor Oils - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Motor-Oils/zgbs/automotive/15719391',

        # # Power Steering Fluids - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Power-Steering-Fluids/zgbs/automotive/15719541',

        # # Refrigerants - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Refrigerants/zgbs/automotive/15719561',

        # # Fluid Sealers - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Fluid-Sealers/zgbs/automotive/15719571',

        # # Gasket Sealers - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Gasket-Sealers/zgbs/automotive/15719581',

        # # Thread Lock Sealers - 50
        # 'http://www.amazon.com/Best-Sellers-Automotive-Thread-Lock-Sealers/zgbs/automotive/15719631',

        # # Transmission Fluids - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Transmission-Fluids/zgbs/automotive/15719641',

        # # Windshield Washer Fluids - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Windshield-Washer-Fluids/zgbs/automotive/15719651',

        


        # # Car Care - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Care/zgbs/automotive/15718271',

        # # Cleaning Kits - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Kits/zgbs/automotive/15718281',

        # # Exterior Care Products - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Exterior-Care-Products/zgbs/automotive/15718291',

        # # Polishes & Waxes - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Polishes-Waxes/zgbs/automotive/15718301',

        # # Chrome & Metal Polishes - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Chrome-Metal-Polishes/zgbs/automotive/15718311',

        # # Chrome Polishes - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Chrome-Polishes/zgbs/automotive/15718321',

        # # Metal Polishes - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Metal-Polishes/zgbs/automotive/15718331',

        # # Pre-Wax Cleaners - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Pre-Wax-Cleaners/zgbs/automotive/15718341',

        # # Bug & Sap Removers - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Bug-Sap-Removers/zgbs/automotive/15718351',

        # # Tar & Wax Removers - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Tar-Wax-Removers/zgbs/automotive/15718361',

        # # Waxes - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Waxes/zgbs/automotive/15718371',

        # # Car Wash Equipment - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Wash-Equipment/zgbs/automotive/15718381',

        # # Car Washing Applicators - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Washing-Applicators/zgbs/automotive/15718391',

        # # Car Washing Buckets - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Washing-Buckets/zgbs/automotive/15718401',

        # # Car Washing Nozzles & Hose Attachments - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Washing-Nozzles-Hose-Attachments/zgbs/automotive/15718411',

        # # Car Washing Sponges & Mitts - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Washing-Sponges-Mitts/zgbs/automotive/15718421',

        # # Waterless Car Washing Treatments - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Waterless-Car-Washing-Treatments/zgbs/automotive/15718431',

        # # Car Washing Windshield Squeegees - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Car-Washing-Windshield-Squeegees/zgbs/automotive/15718441',

        # # Cleaners - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaners/zgbs/automotive/15718451',

        # # Polishing & Rubbing Compounds - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Polishing-Rubbing-Compounds/zgbs/automotive/15718471',

        # # Polishing & Waxing Kits - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Polishing-Waxing-Kits/zgbs/automotive/15718481',

        # # Exterior Sealants - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Exterior-Sealants/zgbs/automotive/15718491',

        # # Cleaning Water Squeegee Blades - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Water-Squeegee-Blades/zgbs/automotive/155340011',

        # # Finishing Products - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Finishing-Products/zgbs/automotive/15718501',

        # # Care Corrosion & Rust Inhibitors - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Care-Corrosion-Rust-Inhibitors/zgbs/automotive/15718511',

        # # Protective Shields - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Protective-Shields/zgbs/automotive/15718521',

        # # Glass Care Products - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Glass-Care-Products/zgbs/automotive/15718531',

        # # Interior Care Products - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Interior-Care-Products/zgbs/automotive/15718541',

        # # Carpet Cleaners - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Carpet-Cleaners/zgbs/automotive/15718551',

        # # Leather Care Products - 70
        # 'http://www.amazon.com/Best-Sellers-Automotive-Leather-Care-Products/zgbs/automotive/15718561',

        # # Protectants - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Protectants/zgbs/automotive/15718571',

        # # Plastic Care Products - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Plastic-Care-Products/zgbs/automotive/15718581',

        # # Rubber Care Products - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Rubber-Care-Products/zgbs/automotive/15718591',

        # # Vinyl Care Products - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Vinyl-Care-Products/zgbs/automotive/15718601',

        # # Upholstery Care Products - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Upholstery-Care-Products/zgbs/automotive/15718611',

        # # Vacuums - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Vacuums/zgbs/automotive/15718621',

        # # Vinyl Cleaners - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Vinyl-Cleaners/zgbs/automotive/318291011',

        # # Solvents - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Solvents/zgbs/automotive/15718631',

        # # Tire & Wheel Care Products - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Tire-Wheel-Care-Products/zgbs/automotive/15718641',

        # # Automotive Tire Care - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Tire-Care/zgbs/automotive/2687786011',

        # # Automotive Wheel Care - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Wheel-Care/zgbs/automotive/2687787011',

        # # Tools & Equipment - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Tools-Equipment/zgbs/automotive/15718651',

        # # Air Dryers, Blowers & Blades - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Air-Dryers-Blowers-Blades/zgbs/automotive/15718661',

        # # Cleaning Brushes & Dusters - 40
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Brushes-Dusters/zgbs/automotive/15718671',

        # # Cleaning Cloths & Towels - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Cloths-Towels/zgbs/automotive/15718681',

        # # Cleaning Chamois - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Chamois/zgbs/automotive/15718691',

        # # Cleaning Drying Mitts - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Drying-Mitts/zgbs/automotive/15718701',

        # # Drying Pads - 20
        # 'http://www.amazon.com/Best-Sellers-Automotive-Drying-Pads/zgbs/automotive/15718711',

        # # Cleaning Microfiber - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Cleaning-Microfiber/zgbs/automotive/15718721',

        # # Detailing Tools - 30
        # 'http://www.amazon.com/Best-Sellers-Automotive-Detailing-Tools/zgbs/automotive/15718731',

        # # Machine Polishing Equipment - 60
        # 'http://www.amazon.com/Best-Sellers-Automotive-Machine-Polishing-Equipment/zgbs/automotive/15718741',

        # # Buffer & Polishing Backing Plates - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Buffer-Polishing-Backing-Plates/zgbs/automotive/15718751',

        # # Body Repair Buffing & Polishing Pads - 80
        # 'http://www.amazon.com/Best-Sellers-Automotive-Body-Repair-Buffing-Polishing-Pads/zgbs/automotive/15707091',

        # # Undercoatings - 10
        # 'http://www.amazon.com/Best-Sellers-Automotive-Undercoatings/zgbs/automotive/15718781',




        # # Laptop Bags, Cases & Sleeves - 50
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Bags-Cases-Sleeves/zgbs/pc/172470',

        # # Laptop Backpacks - 50
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Backpacks/zgbs/pc/335604011',

        # # Laptop Briefcases - 50
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Briefcases/zgbs/pc/3012918011',

        # # Laptop Folio Cases - 50
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Folio-Cases/zgbs/pc/3095279011',

        # # Laptop Messenger Bags - 60
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Messenger-Bags/zgbs/pc/3012920011',

        # # Laptop Shoulder Bags - 60
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Shoulder-Bags/zgbs/pc/3012921011',

        # # Laptop Sleeves - 70
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Sleeves/zgbs/pc/335609011',

        # # Tablet Keyboard Cases - 50
        # 'http://www.amazon.com/Best-Sellers-Computers-Accessories-Tablet-Keyboard-Cases/zgbs/pc/11548963011',
        

        # # Men's Watch Bands - 70
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens-Watch-Bands/zgbs/watches/6358541011',

        # # Women's Watch Bands - 70
        # 'http://www.amazon.com/Best-Sellers-Watches-Womens-Watch-Bands/zgbs/watches/6358545011',

        # # Light Bulbs - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Light-Bulbs/zgbs/hpc/322525011',

        # # Compact Fluorescent Bulbs - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Compact-Fluorescent-Bulbs/zgbs/hpc/328863011',

        # # Fluorescent Tubes - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Fluorescent-Tubes/zgbs/hpc/495232',

        # # Halogen Bulbs - 50
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Halogen-Bulbs/zgbs/hpc/328864011',

        # # High Intensity Discharge Bulbs - 50
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-High-Intensity-Discharge-Bulbs/zgbs/hpc/328871011',

        # # Incandescent Bulbs - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Incandescent-Bulbs/zgbs/hpc/328865011',

        # # Krypton & Xenon Bulbs - 50
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Krypton-Xenon-Bulbs/zgbs/hpc/4910578011',

        # # LED Bulbs - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-LED-Bulbs/zgbs/hpc/2314207011',

        # # Black Light Bulbs - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Black-Light-Bulbs/zgbs/hpc/328867011',


        # # Camera & Photo - 40
        # 'http://www.amazon.com/best-sellers-camera-photo/zgbs/photo',

        # # Surveillance & Security Cameras - 40
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Surveillance-Security-Cameras/zgbs/photo/898400',

        # # Bullet Surveillance Cameras - 20
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Bullet-Surveillance-Cameras/zgbs/photo/14241331',

        # # Dome Surveillance Cameras - 40
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Dome-Surveillance-Cameras/zgbs/photo/14241151',

        # # Hidden Cameras - 20
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Hidden-Cameras/zgbs/photo/12909791',

        # # Simulated Surveillance Cameras - 40
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Simulated-Surveillance-Cameras/zgbs/photo/14241441',




        # # Watches - 40
        # 'http://www.amazon.com/Best-Sellers-Watches/zgbs/watches',

        # # Women's Watches - 20
        # 'http://www.amazon.com/Best-Sellers-Watches-Womens/zgbs/watches/6358543011',

        # # Women's Wrist Watches - 10
        # 'http://www.amazon.com/Best-Sellers-Watches-Womens-Wrist/zgbs/watches/6358544011'

        # # Women's Smartwatches - 20
        # 'http://www.amazon.com/Best-Sellers-Watches-Womens-Smartwatches/zgbs/watches/14130291011',

        # # Men's Watches - 40
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens/zgbs/watches/6358539011',

        # # Men's Wrist Watches - 40
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens-Wrist/zgbs/watches/6358540011',

        # # Men's Watch Bands - 10
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens-Watch-Bands/zgbs/watches/6358541011',

        # # Men's Pocket Watches - 10
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens-Pocket/zgbs/watches/6358542011',

        # # Men's Smartwatches - 20
        # 'http://www.amazon.com/Best-Sellers-Watches-Mens-Smartwatches/zgbs/watches/14130292011',

        # # Girls' Watches - 40
        # 'http://www.amazon.com/Best-Sellers-Watches-Girls/zgbs/watches/6358547011',

        # # Girls' Wrist Watches - 20
        # 'http://www.amazon.com/Best-Sellers-Watches-Girls-Wrist/zgbs/watches/6358548011',

        # # Boys' Watches - 30
        # 'http://www.amazon.com/Best-Sellers-Watches-Boys/zgbs/watches/6358551011',

        # # Boys' Wrist Watches - 30
        # 'http://www.amazon.com/Best-Sellers-Watches-Boys-Wrist/zgbs/watches/6358552011',



        # # Household Supplies - 80
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Supplies/zgbs/hpc/15342811',

        # # Air Freshener Supplies - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Air-Freshener-Supplies/zgbs/hpc/15356121',

        # # Solid & Liquid Air Fresheners - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Solid-Liquid-Air-Fresheners/zgbs/hpc/15347391',

        # # Spray Air Fresheners - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Spray-Air-Fresheners/zgbs/hpc/15356221',

        # # Electric Air Fresheners - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Electric-Air-Fresheners/zgbs/hpc/15356231',

        # # Household Cleaning Tools - 60
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Cleaning-Tools/zgbs/hpc/15342831',

        # # Household Cleaning Brushes - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Cleaning-Brushes/zgbs/hpc/15342891',

        # # Dusting Tools - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Dusting-Tools/zgbs/hpc/15356181',

        # # Feather Dusters - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Feather-Dusters/zgbs/hpc/2245498011',

        # # Dust Cloths - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Dust-Cloths/zgbs/hpc/2245499011',

        # # Household Dust Mops & Pads - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Dust-Mops-Pads/zgbs/hpc/2245876011',

        # # Household Cleaning Gloves - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Cleaning-Gloves/zgbs/hpc/15342901',

        # # Latex Gloves - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Latex-Gloves/zgbs/hpc/15755321',

        # # Nitrile Gloves - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Nitrile-Gloves/zgbs/hpc/15755331',

        # # Vinyl Gloves - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Vinyl-Gloves/zgbs/hpc/15751151',

        # # Household Mops, Buckets & Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Mops-Buckets-Accessories/zgbs/hpc/2245503011',

        # # Household Wet Mops - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Wet-Mops/zgbs/hpc/2245507011',

        # # Household Mop Buckets - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Mop-Buckets/zgbs/hpc/2245509011',

        # # Household Mop Heads & Handles - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Mop-Heads-Handles/zgbs/hpc/2245508011',

        # # Household Cleaning Sponges - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Cleaning-Sponges/zgbs/hpc/15754811',

        # # Household Squeegees - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Squeegees/zgbs/hpc/2245500011',

        # # Household Brooms, Dustpans & Accessories - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Brooms-Dustpans-Accessories/zgbs/hpc/2245502011',

        # # Household Brooms - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Brooms/zgbs/hpc/2245510011',

        # # Household Angle Brooms - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Angle-Brooms/zgbs/hpc/14253831',

        # # Household Push Brooms - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Push-Brooms/zgbs/hpc/14253851',

        # # Household Dustpans - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Dustpans/zgbs/hpc/2245512011',

        # # Dishwashing Supplies - 50
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Dishwashing-Supplies/zgbs/hpc/15693761',

        # # Dish Detergent - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Dish-Detergent/zgbs/hpc/15342851',

        # # Dishwasher Detergent - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Dishwasher-Detergent/zgbs/hpc/15693671',

        # # Household Scouring Pads - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Scouring-Pads/zgbs/hpc/2245501011',

        # # Household Cleaning - 70
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Cleaning/zgbs/hpc/15342821',

        # # All-Purpose Household Cleaners - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-All-Purpose-Household-Cleaners/zgbs/hpc/15356141',

        # # Bathroom Cleaners - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Bathroom-Cleaners/zgbs/hpc/15347371',

        # # Household Carpet Cleaners & Deodorizers - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Household-Carpet-Cleaners-Deodorizers/zgbs/hpc/361410011',

        # # Laundry Supplies - 60
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Laundry-Supplies/zgbs/hpc/15356111',

        # # Powder Laundry Detergent - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Powder-Laundry-Detergent/zgbs/hpc/15342921',

        # # Liquid Laundry Detergent - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Liquid-Laundry-Detergent/zgbs/hpc/15342931',

        # # Laundry Bleach - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Laundry-Bleach/zgbs/hpc/15342941',

        # # Fabric Softener - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Fabric-Softener/zgbs/hpc/15356191',

        # # Starch & Anti-static Sprays - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Starch-Anti-static-Sprays/zgbs/hpc/15342951',

        # # Lint Removal - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Lint-Removal/zgbs/hpc/15342961',

        # # Fabric Deodorizer - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Fabric-Deodorizer/zgbs/hpc/15356201',

        # # Laundry Stain Removal - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Laundry-Stain-Removal/zgbs/hpc/15356211',

        # # Light Bulbs - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Light-Bulbs/zgbs/hpc/322525011',

        # # Compact Fluorescent Bulbs - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Compact-Fluorescent-Bulbs/zgbs/hpc/328863011',

        # # Fluorescent Tubes - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Fluorescent-Tubes/zgbs/hpc/495232',

        # # Halogen Bulbs - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Halogen-Bulbs/zgbs/hpc/328864011',

        # # Incandescent Bulbs - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Incandescent-Bulbs/zgbs/hpc/328865011',

        # # LED Bulbs - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-LED-Bulbs/zgbs/hpc/2314207011',

        # # Lighters & Matches - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Lighters-Matches/zgbs/hpc/10342347011',

        # # Lighters - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Lighters/zgbs/hpc/10342354011',

        # # Paper & Plastic Household Supplies - 60
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Paper-Plastic-Household-Supplies/zgbs/hpc/15342841',

        # # Trash Bags - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Trash-Bags/zgbs/hpc/15342971',

        # # Tall Kitchen Bags - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Tall-Kitchen-Bags/zgbs/hpc/15751141',

        # # Large Kitchen Bags - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Large-Kitchen-Bags/zgbs/hpc/15755301',

        # # Bath Tissue - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Bath-Tissue/zgbs/hpc/15342981',

        # # Paper Towels - 40
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Paper-Towels/zgbs/hpc/15347401',

        # # Paper Facial Tissues - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Paper-Facial-Tissues/zgbs/hpc/15356241',

        # # Disposable Plates & Cutlery - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Disposable-Plates-Cutlery/zgbs/hpc/15342991',

        # # Disposable Forks - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Disposable-Forks/zgbs/hpc/15757571',

        # # Disposable Sporks - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Disposable-Sporks/zgbs/hpc/15754781',

        # # Cups & Straws - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Cups-Straws/zgbs/hpc/15343011',

        # # Disposable Food Storage Products - 50
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Disposable-Food-Storage-Products/zgbs/hpc/15377691',

        # # Coffee Filters - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Coffee-Filters/zgbs/hpc/14042401',

        # # Reusable Coffee Filters - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Reusable-Coffee-Filters/zgbs/hpc/14162591',

        


        # # Baby & Child Health Care Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Child-Products/zgbs/hpc/16025501',

        # # Children's Vitamins - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Childrens-Vitamins/zgbs/hpc/16225031',

        # # Baby & Child Personal Care Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Child-Products/zgbs/hpc/16025511',

        # # Baby Bathing Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Bathing-Products/zgbs/hpc/16023581',

        # # Baby Skin Care - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Skin/zgbs/hpc/166740011',

        # # Diaper Creams - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Diaper-Creams/zgbs/hpc/322263011',

        # # Baby Lotions - 20
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Lotions/zgbs/hpc/322264011',

        # # Baby Oils - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Oils/zgbs/hpc/322265011',

        # # Baby Powders - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Powders/zgbs/hpc/322266011',

        # # Baby Toothbrushes - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Toothbrushes/zgbs/hpc/7909329011',

        # # Hair Care for Children - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Hair-Children/zgbs/hpc/16027261',

        # # Nursing Pads - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Nursing-Pads/zgbs/hpc/16225011',

        # # Kid's Oral Hygiene Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Kids-Oral-Hygiene-Products/zgbs/hpc/16023601',

        # # Health Care Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Products/zgbs/hpc/3760941',

        # # Alternative Medicine Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Alternative-Medicine-Products/zgbs/hpc/13052911',

        # # Ayurveda Products - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Ayurveda-Products/zgbs/hpc/13052941',

        # # Light Therapy Products - 5
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Light-Therapy-Products/zgbs/hpc/13053141',

        # # Manipulation Therapy Products - 30
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Manipulation-Therapy-Products/zgbs/hpc/13053161',

        # # Single Homeopathic Remedies - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Single-Homeopathic-Remedies/zgbs/hpc/3767781',

        # # Sound Therapy Products - 10
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Sound-Therapy-Products/zgbs/hpc/13052981',

        # # Office Electronics Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Office-Products/zgbs/electronics/172574',

        # # Security & Surveillance Equipment
        # 'http://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136',

        # # Outlet
        # 'http://www.amazon.com/Best-Sellers-Electronics-Outlet/zgbs/electronics/301793',

        # # Portable Audio & Video
        # 'http://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623',

        # # Televisions & Video Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011',

        # # Video Game Consoles & Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011',

        # # Electronics Accessories & Supplies
        # 'http://www.amazon.com/Best-Sellers-Electronics-Accessories-Supplies/zgbs/electronics/281407',

        # # Cell Phone Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011',

        # # Computer Accessories & Peripherals
        # 'http://www.amazon.com/Best-Sellers-Electronics-Computer-Accessories-Peripherals/zgbs/electronics/172456',

        # # Blank Media Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Blank-Media-Products/zgbs/electronics/281408',

        # # Electronics Cables
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cables/zgbs/electronics/12954861',

        # # Recording Microphones & Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Recording-Microphones-Accessories/zgbs/electronics/11974521',

        # # Electronics Power Protection Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Power-Protection-Products/zgbs/electronics/2223901011',

        # # Electrical Cord Management
        # 'http://www.amazon.com/Best-Sellers-Electronics-Electrical-Cord-Management/zgbs/electronics/11042051',

        # # School Adhesives
        # 'http://www.amazon.com/Best-Sellers-Office-Products-School-Adhesives/zgbs/office-products/1068992',

        # # Art Supplies & Craft Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Art-Supplies-Craft/zgbs/office-products/490778011',

        # # Filing Products
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Filing/zgbs/office-products/1069554',

        # # Math Materials
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Math-Materials/zgbs/office-products/12900191',

        # # Appliances
        # 'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances',

        # #####################

        # # Beauty
        # 'http://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty',

        # # Bath & Body Care
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Body-Care/zgbs/beauty/11055991',

        # # Bath Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Products/zgbs/beauty/11056211',

        # # Bath Salts
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Salts/zgbs/beauty/11056251',

        # # Bath Oils
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Oils/zgbs/beauty/11056261',

        # # Bathing Accessories
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bathing-Accessories/zgbs/beauty/11056491',

        # # Bath & Body Brushes
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Body-Brushes/zgbs/beauty/11056501',

        # # Bath Loofahs & Body Sponges
        # 'http://www.amazon.com/Best-Sellers-Beauty-Bath-Loofahs-Body-Sponges/zgbs/beauty/11056551',

        # # Hair Drying Towels
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Drying-Towels/zgbs/beauty/3784491',

        # # Body Cleansers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Cleansers/zgbs/beauty/11056281',

        # # Hair Removal Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Products/zgbs/beauty/3779051',

        # # Hair Removal Tweezers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Tweezers/zgbs/beauty/3779181',

        # # Hair Removal Waxing Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Waxing-Products/zgbs/beauty/3779191',

        # # Hands, Feet & Nail Care
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hands-Feet-Nail-Care/zgbs/beauty/11062211',

        # # Callus Shavers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Callus-Shavers/zgbs/beauty/11063571',

        # # Cuticle Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Cuticle-Care-Products/zgbs/beauty/11062221',

        # # Hand Creams & Lotions
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hand-Creams-Lotions/zgbs/beauty/11062261',

        # # Hand Soaps
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hand-Soaps/zgbs/beauty/11062271',

        # # Nail Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Care-Products/zgbs/beauty/11062291',

        # # Nail Growth Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Growth-Products/zgbs/beauty/11062311',

        # # Nail Repair
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Repair/zgbs/beauty/11062321',

        # # Nail Strengtheners
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Strengtheners/zgbs/beauty/11062331',

        # # Lip Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Lip-Care-Products/zgbs/beauty/3761351',

        # # Lip Balms & Moisturizers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Lip-Balms-Moisturizers/zgbs/beauty/979546011',

        # # Body Moisturizers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Moisturizers/zgbs/beauty/11060661',

        # # Body Butter
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Butter/zgbs/beauty/11060671',

        # # Body Creams
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Creams/zgbs/beauty/11060681',

        # # Body Lotions
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Lotions/zgbs/beauty/14024031',

        # # Body Oils
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Oils/zgbs/beauty/11060691',

        # # Body Scrubs & Treatments
        # 'http://www.amazon.com/Best-Sellers-Beauty-Body-Scrubs-Treatments/zgbs/beauty/11056421',

        # # Perfumes & Fragrances
        # 'http://www.amazon.com/Best-Sellers-Beauty-Perfumes-Fragrances/zgbs/beauty/11056591',

        # # Women's Fragrances
        # 'http://www.amazon.com/Best-Sellers-Beauty-Womens-Fragrances/zgbs/beauty/11056931',

        # # Hair Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Care-Products/zgbs/beauty/11057241',

        # # Hair Shampoo
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Shampoo/zgbs/beauty/11057651',

        # # Hair Conditioner
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Conditioner/zgbs/beauty/11057251',

        # # Hair Styling Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Styling-Products/zgbs/beauty/11057841',

        # # Hair Coloring Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Coloring-Products/zgbs/beauty/11057451',

        # # Hair & Scalp Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Scalp-Care-Products/zgbs/beauty/10666241011',

        # # Hair & Scalp Treatments
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Scalp-Treatments/zgbs/beauty/11057431',

        # # Hair Loss Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Loss-Products/zgbs/beauty/10898755011',

        # # Hair Relaxers & Texturizers
        # 'http://www.amazon.com/Best-Sellers-Beauty-Hair-Relaxers-Texturizers/zgbs/beauty/10702858011',

        # # Makeup
        # 'http://www.amazon.com/Best-Sellers-Beauty-Makeup/zgbs/beauty/11058281',

        # # Eye Makeup
        # 'http://www.amazon.com/Best-Sellers-Beauty-Eye-Makeup/zgbs/beauty/11058331',

        # # Face Makeup
        # 'http://www.amazon.com/Best-Sellers-Beauty-Face-Makeup/zgbs/beauty/11058691',

        # # Lip Makeup
        # 'http://www.amazon.com/Best-Sellers-Beauty-Lip-Makeup/zgbs/beauty/11059031',

        # # Makeup Remover
        # 'http://www.amazon.com/Best-Sellers-Beauty-Makeup-Remover/zgbs/beauty/11059231',

        # # Nail Polish & Nail Decoration Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Polish-Decoration-Products/zgbs/beauty/11059311',

        # # Nail Top & Base Coats
        # 'http://www.amazon.com/Best-Sellers-Beauty-Nail-Top-Base-Coats/zgbs/beauty/11059361',

        # # Skin Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Skin-Care-Products/zgbs/beauty/11060451',

        # # Eye Treatment Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Eye-Treatment-Products/zgbs/beauty/11061941',

        # # Facial Skin Care Products
        # 'http://www.amazon.com/Best-Sellers-Beauty-Facial-Skin-Care-Products/zgbs/beauty/11060711',

        # # Maternity Skin Care
        # 'http://www.amazon.com/Best-Sellers-Beauty-Maternity-Skin-Care/zgbs/beauty/11062371',

        # # Beauty Tools & Accessories
        # 'http://www.amazon.com/Best-Sellers-Beauty-Tools-Accessories/zgbs/beauty/11062741',

        # # Makeup Brushes & Tools
        # 'http://www.amazon.com/Best-Sellers-Beauty-Makeup-Brushes-Tools/zgbs/beauty/11059391',

        # # Cotton Balls & Swabs
        # 'http://www.amazon.com/Best-Sellers-Beauty-Cotton-Balls-Swabs/zgbs/beauty/3784921',

        # #####################

        # # Office Products
        # 'http://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products',

        # # Education Supplies & Craft Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Education-Supplies-Craft/zgbs/office-products/12899801',

        # # Mail Supplies & Shipping Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Mail-Supplies-Shipping/zgbs/office-products/1068972',

        # # Office & School Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-School-Supplies/zgbs/office-products/1069242',

        # #####################
        
        # # Coffee, Tea & Espresso
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Tea-Espresso/zgbs/home-garden/915194',

        # # Coffee & Tea
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Tea/zgbs/home-garden/7083296011',

        # # Coffee Beverages
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Beverages/zgbs/home-garden/16318031',

        # # Tea Beverages
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Tea-Beverages/zgbs/home-garden/16318401',

        # # Dry Dog Food
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dry-Dog-Food/zgbs/pet-supplies/2975360011',

        # # Dog Treats
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Treats/zgbs/pet-supplies/2975434011',

        # # Dry Cat Food
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dry-Cat-Food/zgbs/pet-supplies/2975266011',

        # # Cat Treats
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Cat-Treats/zgbs/pet-supplies/2975309011',

        # # Baby & Toddler Feeding Supplies
        # 'http://www.amazon.com/Best-Sellers-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011',

        # # Pregnancy & Maternity Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Pregnancy-Maternity-Products/zgbs/baby-products/166804011',

        # # Baby Gear
        # 'http://www.amazon.com/Best-Sellers-Baby-Gear/zgbs/baby-products/166828011',

        # # Baby Health & Care Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Health-Care-Products/zgbs/baby-products/166856011',

        # # Baby Safety Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Safety-Products/zgbs/baby-products/166863011',

        # # Cell Phone Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011',

        # # Cell Phone Batteries & Battery Packs
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Batteries-Battery-Packs/zgbs/electronics/2407758011',

        # # Bluetooth Cell Phone Headsets
        # 'http://www.amazon.com/Best-Sellers-Electronics-Bluetooth-Cell-Phone-Headsets/zgbs/electronics/2407776011',

        # # Wired Cell Phone Headsets
        # 'http://www.amazon.com/Best-Sellers-Electronics-Wired-Cell-Phone-Headsets/zgbs/electronics/2407777011',

        # #####################

        # 'http://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games',
        # 'http://www.amazon.com/Best-Sellers-Music-CDs-Vinyl/zgbs/music/5174',
        # 'http://www.amazon.com/best-sellers-video-games/zgbs/videogames',
        # 'http://www.amazon.com/best-sellers-video-games/zgbs/books',

        # #####################

        # 'http://www.amazon.com/gp/bestsellers/pc/541966/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Data-Storage/zgbs/electronics/1292110011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Laptop-Accessories/zgbs/electronics/3011391011/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Dolls-Accessories/zgbs/toys-and-games/166118011/',

        # #####################

        # 'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/',
        # 'http://www.amazon.com/best-sellers-camera-photo/zgbs/photo/',
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Bags-Cases/zgbs/photo/172437/',
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Tripod-Monopod-Cases/zgbs/photo/3346131/',
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Telescope-Cases/zgbs/photo/3346091/',
        # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Video-Projector-Cases/zgbs/photo/1205270/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Bath-Products/zgbs/home-garden/1063236/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Store/zgbs/home-garden/3206325011/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Baking-Supplies/zgbs/home-garden/2231407011/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bedding/zgbs/home-garden/1063268/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Nursery-Bedding/zgbs/home-garden/166742011/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Child-Products/zgbs/hpc/16025501/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Products/zgbs/hpc/3760941/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Alternative-Medicine-Products/zgbs/hpc/13052911/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Acupuncture-Products/zgbs/hpc/13052921/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Ayurveda-Products/zgbs/hpc/13052941/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Flower-Essences/zgbs/hpc/3767761/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Light-Therapy-Products/zgbs/hpc/13053141/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Manipulation-Therapy-Products/zgbs/hpc/13053161/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Oxygen-Therapy-Products/zgbs/hpc/13052971/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Single-Homeopathic-Remedies/zgbs/hpc/3767781/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Sound-Therapy-Products/zgbs/hpc/13052981/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Foot-Products/zgbs/hpc/3779911/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Moleskin/zgbs/hpc/3779981/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Foot-Odor-Control-Products/zgbs/hpc/3780131/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Wart-Removal-Products/zgbs/hpc/3780171/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Corn-Callus-Trimmers/zgbs/hpc/3779971/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Diabetic-Foot/zgbs/hpc/3780001/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Furniture/zgbs/home-garden/1063306/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bath/zgbs/home-garden/3263108011/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bath-Towels/zgbs/home-garden/3263111011/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Shower-Accessories/zgbs/home-garden/3265576011/',
        # 'http://www.amazon.com/Best-Sellers-Watches/zgbs/watches/',
        # 'http://www.amazon.com/gp/bestsellers/toys-and-games/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Figures-Playsets/zgbs/toys-and-games/165993011/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Toy-Figures/zgbs/toys-and-games/2514571011/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Figure-Vehicles-Playsets/zgbs/toys-and-games/7620514011/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Figure-Vehicles/zgbs/toys-and-games/274293011/',
        # 'http://www.amazon.com/gp/bestsellers/pc/541966/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-External-Components/zgbs/electronics/3012292011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-External-Sound-Cards/zgbs/electronics/3015427011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-External-TV-Tuners/zgbs/electronics/3015428011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Graphics-Card-Fans/zgbs/electronics/3015421011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Water-Cooling-Systems/zgbs/electronics/3015422011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Internal-Hard-Drive-Cooling-Fans/zgbs/electronics/3228286011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/',
        
        # 'http://www.amazon.com/gp/bestsellers/books/',
        # 'http://www.amazon.com/gp/bestsellers/wireless/',
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_bestseller', start_urls=start_urls, premium=True)
    # process.crawl('amazon_bestseller_sub', start_urls=start_urls)
    process.start()
