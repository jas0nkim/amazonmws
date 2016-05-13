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
        # Fiber Optic Products - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fiber-Optic-Products/zgbs/industrial/306611011',

        # Fiber Optic Transceivers - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fiber-Optic-Transceivers/zgbs/industrial/306627011',

        # Lighting Components - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lighting-Components/zgbs/industrial/6355949011',

        # Electrical Ballasts - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Ballasts/zgbs/industrial/5789850011',

        # Light Sockets - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Light-Sockets/zgbs/industrial/14328101',

        # Recessed Light Fixtures - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Recessed-Light-Fixtures/zgbs/industrial/3736711',

        # Recessed Lighting Housings - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Recessed-Lighting-Housings/zgbs/industrial/5486419011',

        # Recessed Lighting Trims - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Recessed-Lighting-Trims/zgbs/industrial/5486420011',

        # Recessed Lighting Housing & Trim Kits - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Recessed-Lighting-Housing-Trim-Kits/zgbs/industrial/5486421011',

        # Optoelectronic Products - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Optoelectronic-Products/zgbs/industrial/306743011',

        # LEDs - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-LEDs/zgbs/industrial/306760011',

        # Lamp Holders - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lamp-Holders/zgbs/industrial/306746011',

        # Optoelectronic Lamps - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Optoelectronic-Lamps/zgbs/industrial/306747011',

        # Arc Lamps - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Arc-Lamps/zgbs/industrial/306748011',

        # Fluorescent Lamps - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fluorescent-Lamps/zgbs/industrial/306749011',

        # HID Lamps - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-HID-Lamps/zgbs/industrial/306750011',

        # Incandescent Lamps - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Incandescent-Lamps/zgbs/industrial/306751011',

        # LED Lamps - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-LED-Lamps/zgbs/industrial/306752011',

        # Optoelectronic Displays - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Optoelectronic-Displays/zgbs/industrial/306754011',

        # Photo Detectors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Photo-Detectors/zgbs/industrial/306766011',

        # Passive Components - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Passive-Components/zgbs/industrial/306767011',

        # Antennas - 25
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Antennas/zgbs/industrial/306768011',

        # Capacitors - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Capacitors/zgbs/industrial/306788011',

        # Electronic Ferrites - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Ferrites/zgbs/industrial/306792011',

        # Electronic Inductors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Inductors/zgbs/industrial/306793011',

        # Resistors - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Resistors/zgbs/industrial/306804011',

        # Fixed Resistors - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fixed-Resistors/zgbs/industrial/306805011',

        # Variable Resistors - 15
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Variable-Resistors/zgbs/industrial/306809011',

        # Potentiometers - 10,
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Potentiometers/zgbs/industrial/306810011',

        # Signal Filters - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Signal-Filters/zgbs/industrial/306813011',

        # Transformers - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Transformers/zgbs/industrial/306828011',

        # Power Transformers - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Transformers/zgbs/industrial/306830011',

        # Semiconductor Products - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Semiconductor-Products/zgbs/industrial/306831011',

        # Diodes - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Diodes/zgbs/industrial/306838011',

        # Interfaces - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Interfaces/zgbs/industrial/306842011',

        # Microprocessors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Microprocessors/zgbs/industrial/306872011',

        # Signal Components - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Signal-Components/zgbs/industrial/306873011',

        # Signal Amplifiers - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Signal-Amplifiers/zgbs/industrial/306874011',

        # Signal Converters - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Signal-Converters/zgbs/industrial/306896011',

        # Semiconductor Timing Management Products - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Semiconductor-Timing-Management-Products/zgbs/industrial/306899011',

        # Transistors - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Transistors/zgbs/industrial/306910011',

        # Electronic Component Sensors - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Component-Sensors/zgbs/industrial/306923011',

        # Flow Sensors - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flow-Sensors/zgbs/industrial/306928011',

        # Motion Detectors - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Motion-Detectors/zgbs/industrial/11040971',

        # Photoelectric Sensors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Photoelectric-Sensors/zgbs/industrial/306933011',

        # Proximity Sensors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Proximity-Sensors/zgbs/industrial/306936011',

        # Temperature Probes & Sensors - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Temperature-Probes-Sensors/zgbs/industrial/5006547011'

        # Thermal Management Products - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermal-Management-Products/zgbs/industrial/306943011',

        # Computer Heatsinks - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Computer-Heatsinks/zgbs/industrial/306944011',

        # Electronic Cooling Fans - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Cooling-Fans/zgbs/industrial/306945011',

        # Computer Case Fans - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Computer-Case-Fans/zgbs/industrial/11036291',

        # Interconnects - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Interconnects/zgbs/industrial/306629011',

        # Interconnect Cables - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Interconnect-Cables/zgbs/industrial/306641011',

        # Multiconductor Cables - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Multiconductor-Cables/zgbs/industrial/306677011',

        # Computer Cables & Interconnects - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Computer-Cables-Interconnects/zgbs/industrial/172463',

        # Ethernet Cables - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ethernet-Cables/zgbs/industrial/464398',

        # Lightning Cables - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lightning-Cables/zgbs/industrial/6795233011',

        # Audio & Video Power Cables - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Audio-Video-Power-Cables/zgbs/industrial/597260',

        # SATA Cables - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-SATA-Cables/zgbs/industrial/3015394011',

        # Thunderbolt Cables - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thunderbolt-Cables/zgbs/industrial/6795232011',

        # USB Cables - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-USB-Cables/zgbs/industrial/464394',

        # Computer VGA Cables - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Computer-VGA-Cables/zgbs/industrial/15782091',

        # Connectors - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Connectors/zgbs/industrial/5739460011',

        # Circular Connectors - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Circular-Connectors/zgbs/industrial/5739461011',

        # Cylindrical Connectors - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cylindrical-Connectors/zgbs/industrial/5739462011',

        # Fiber Optic Connectors - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fiber-Optic-Connectors/zgbs/industrial/306612011',

        # Electrical Boxes, Conduit & Fittings - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Boxes-Conduit-Fittings/zgbs/industrial/6369359011',

        # Electrical Brackets - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Brackets/zgbs/industrial/6369372011',

        # Electrical Boxes - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Boxes/zgbs/industrial/495308',

        # Electrical Outlet Boxes - 60
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Outlet-Boxes/zgbs/industrial/6369374011',

        # Extension Cords - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Extension-Cords/zgbs/industrial/495312',

        # Industrial Heat-shrink Tubing - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Heat-shrink-Tubing/zgbs/industrial/700782011',

        # Isolation Transformers - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Isolation-Transformers/zgbs/industrial/10967671',

        # Electric Outlets & Accessories - 80
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Outlets-Accessories/zgbs/industrial/495334',

        # Ground Fault Circuit Interrupter Outlets - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ground-Fault-Circuit-Interrupter-Outlets/zgbs/industrial/6291366011',

        # Electrical Outlet Covers - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Outlet-Covers/zgbs/industrial/6291367011',

        # Electrical Outlet Switches - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Outlet-Switches/zgbs/industrial/6291368011',

        # RV Receptacles - 30
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-RV-Receptacles/zgbs/industrial/6359402011',

        # Standard Electrical Outlets - 70
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Standard-Electrical-Outlets/zgbs/industrial/6291365011',

        # Terminal Blocks - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Terminal-Blocks/zgbs/industrial/306708011',

        # Fuse Blocks - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Blocks/zgbs/industrial/306712011',

        # Thermocouple Blocks - 15
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermocouple-Blocks/zgbs/industrial/306717011',

        # Interconnect Terminals - 40
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Interconnect-Terminals/zgbs/industrial/306719011',

        # Butt Terminals - 20
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Butt-Terminals/zgbs/industrial/306720011',

        # Disconnect Terminals - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disconnect-Terminals/zgbs/industrial/306723011',

        # IDC Electrical Terminals - 10
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-IDC-Electrical-Terminals/zgbs/industrial/306727011',

        # Screw Terminals - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Screw-Terminals/zgbs/industrial/306731011',

        # Spade Terminals - 5
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spade-Terminals/zgbs/industrial/306733011',

        # Electrical Wire - 50
        'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Wire/zgbs/industrial/495310',




        # # Hydraulics, Pneumatics & Plumbing - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulics-Pneumatics-Plumbing/zgbs/industrial/3021479011',

        # # Industrial Cylinders & Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cylinders-Accessories/zgbs/industrial/4650338011',

        # # Hydraulic Cylinder Accessories - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Cylinder-Accessories/zgbs/industrial/4650339011',

        # # Hydraulic Lifting Cylinders - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Lifting-Cylinders/zgbs/industrial/256361011',

        # # Pneumatic Accessories - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pneumatic-Accessories/zgbs/industrial/1265135011',

        # # Pneumatic Air Cylinders - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pneumatic-Air-Cylinders/zgbs/industrial/1265133011',

        # # Hydraulic Cylinders - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Cylinders/zgbs/industrial/3754101',

        # # Fittings - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fittings/zgbs/industrial/3021480011',

        # # Expansion Plugs - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Expansion-Plugs/zgbs/industrial/979140011',

        # # Hose Fittings - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hose-Fittings/zgbs/industrial/383665011',

        # # Barbed Hose Fittings - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barbed-Hose-Fittings/zgbs/industrial/6001529011',

        # # Cam & Groove Hose Fittings - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cam-Groove-Hose-Fittings/zgbs/industrial/580142011',

        # # Fire Hose Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fire-Hose-Fittings/zgbs/industrial/7236044011',

        # # Hose Clamps - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hose-Clamps/zgbs/industrial/256338011',

        # # Band Hose Clamps - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Band-Hose-Clamps/zgbs/industrial/6001524011',

        # # Ear Clamps - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ear-Clamps/zgbs/industrial/979135011',

        # # Hose Clamping Tools - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hose-Clamping-Tools/zgbs/industrial/6001526011',

        # # Snap Grip Hose Clamps - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Snap-Grip-Hose-Clamps/zgbs/industrial/979132011',

        # # Spring Hose Clamps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spring-Hose-Clamps/zgbs/industrial/6001523011',

        # # T-Bolt Hose Clamps - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bolt-Hose-Clamps/zgbs/industrial/979131011',

        # # Worm Gear Hose Clamps - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Worm-Gear-Hose-Clamps/zgbs/industrial/979130011',

        # # Hydraulic Hose Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Hose-Fittings/zgbs/industrial/6001531011',

        # # Push-On Hose Fittings - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Push-Hose-Fittings/zgbs/industrial/6001528011',

        # # Quick Connect Hose Fittings - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Quick-Connect-Hose-Fittings/zgbs/industrial/6001527011',

        # # Universal Hose Fittings - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Universal-Hose-Fittings/zgbs/industrial/6001530011',

        # # Pipe Fittings - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pipe-Fittings/zgbs/industrial/383612011',

        # # Tube Fittings - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tube-Fittings/zgbs/industrial/383602011',

        # # Barbed Fittings - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barbed-Fittings/zgbs/industrial/383604011',

        # # Barbed Y Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barbed-Fittings/zgbs/industrial/700728011',

        # # Barbed Elbow Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barbed-Elbow-Fittings/zgbs/industrial/700729011',

        # # Barbed Tee Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barbed-Tee-Fittings/zgbs/industrial/700732011',

        # # Compression Fittings - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Fittings/zgbs/industrial/383614011',

        # # Compression Bulkhead Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Bulkhead-Fittings/zgbs/industrial/700755011',

        # # Compression Cross Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Cross-Fittings/zgbs/industrial/700757011',

        # # Compression Fitting Ferrules - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Fitting-Ferrules/zgbs/industrial/700759011',

        # # Compression Fitting Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Fitting-Nuts/zgbs/industrial/700760011',

        # # Compression Fitting Tube Inserts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Fitting-Tube-Inserts/zgbs/industrial/700762011',

        # # Compression Union Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Union-Fittings/zgbs/industrial/700763011',

        # # Compression Union Reducers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Union-Reducers/zgbs/industrial/700764011',

        # # Compression Union Straights - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compression-Union-Straights/zgbs/industrial/700765011',

        # # Flared Tube Fittings - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flared-Tube-Fittings/zgbs/industrial/5760572011',

        # # Luer Fittings - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-Fittings/zgbs/industrial/383606011',

        # # Luer-to-barbed Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-barbed-Fittings/zgbs/industrial/383608011',

        # # Luer-to-barbed Bulkhead Fittings - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-barbed-Bulkhead-Fittings/zgbs/industrial/700786011',

        # # Luer-to-barbed Elbow Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-barbed-Elbow-Fittings/zgbs/industrial/700788011',

        # # Luer Cap Fittings - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-Cap-Fittings/zgbs/industrial/700746011',

        # # Luer Lock Rings - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Luer-Lock-Rings/zgbs/industrial/700748011',

        # # Microbore Tubing Connectors - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Microbore-Tubing-Connectors/zgbs/industrial/580145011',

        # # Push-to-connect Fittings - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Push-connect-Fittings/zgbs/industrial/580146011',

        # # Quick-connect Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Quick-connect-Fittings/zgbs/industrial/383609011',

        # # Quick-connect-to-barbed Fittings - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Quick-connect-barbed-Fittings/zgbs/industrial/383610011',

        # # Sanitary Fittings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanitary-Fittings/zgbs/industrial/580147011',

        # # Threaded Tube Fittings - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threaded-Tube-Fittings/zgbs/industrial/383603011',

        # # Flowmeters - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flowmeters/zgbs/industrial/3206433011',

        # # Flow Switches - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flow-Switches/zgbs/industrial/4650340011',

        # # Industrial Hose Nozzles - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hose-Nozzles/zgbs/industrial/5760175011',

        # # Industrial Dispensing Nozzles - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Dispensing-Nozzles/zgbs/industrial/5760178011',

        # # Industrial Fire Hose Nozzles - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fire-Hose-Nozzles/zgbs/industrial/5760177011',

        # # Industrial Hose Washdown Nozzles - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hose-Washdown-Nozzles/zgbs/industrial/5760176011',

        # # Hydraulic Equipment - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Equipment/zgbs/industrial/3754081',

        # # Hydraulic Adapters - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Adapters/zgbs/industrial/383871011',

        # # Hydraulic Couplings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Couplings/zgbs/industrial/383873011',

        # # Hydraulic Fittings - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Fittings/zgbs/industrial/383874011',

        # # Hydraulic Gauges - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Gauges/zgbs/industrial/3754111',

        # # Hydraulic Motors - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Motors/zgbs/industrial/383875011',

        # # Hydraulic Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Pumps/zgbs/industrial/3754141',

        # # Hydraulic Tanks & Reservoirs - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Tanks-Reservoirs/zgbs/industrial/3754151',

        # # Hydraulic Valves - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Valves/zgbs/industrial/383870011',

        # # Industrial Pumps - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pumps/zgbs/industrial/1265113011',

        # # Diaphragm Pumps - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Diaphragm-Pumps/zgbs/industrial/1265115011',

        # # Drum Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drum-Pumps/zgbs/industrial/1265118011',

        # # Flexible Impeller Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flexible-Impeller-Pumps/zgbs/industrial/1265120011',

        # # Gear Pumps - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Gear-Pumps/zgbs/industrial/1265114011',

        # # Jet Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Jet-Pumps/zgbs/industrial/1265122011',

        # # Submersible Pumps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Submersible-Pumps/zgbs/industrial/1265116011',

        # # Push-In Plugs - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Push-Plugs/zgbs/industrial/4650342011',

        # # Seals & O-Rings - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Seals-Rings/zgbs/industrial/16413421',

        # # Bearing Isolators - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bearing-Isolators/zgbs/industrial/16411131',

        # # Diaphragm Seals - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Diaphragm-Seals/zgbs/industrial/16413461',

        # # Door Seals - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Door-Seals/zgbs/industrial/16413471',

        # # Gaskets - 25
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Gaskets/zgbs/industrial/16413481',

        # # Sheet & Die-Cut Gaskets - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sheet-Die-Cut-Gaskets/zgbs/industrial/16413521',

        # # Spring Finger Gaskets - 1
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spring-Finger-Gaskets/zgbs/industrial/16413541',

        # # Tape Gaskets - 25
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tape-Gaskets/zgbs/industrial/16413551',

        # # Window Gaskets - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Window-Gaskets/zgbs/industrial/16413561',

        # # O-Rings - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rings/zgbs/industrial/16413611',

        # # Radial Shaft Seals - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Radial-Shaft-Seals/zgbs/industrial/16413621',

        # # Strapping Seals & Sealers - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Strapping-Seals-Sealers/zgbs/industrial/16413641',

        # # Tubing, Pipe, and Hose - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tubing-Pipe-Hose/zgbs/industrial/9631359011',

        # # Industrial Hoses - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hoses/zgbs/industrial/256330011',

        # # Air Tool Hose Reels - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Air-Tool-Hose-Reels/zgbs/industrial/552278',

        # # Air Tool Hoses - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Air-Tool-Hoses/zgbs/industrial/552280',

        # # Industrial Chemical Hoses - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Chemical-Hoses/zgbs/industrial/256334011',

        # # Industrial Duct Hoses - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Duct-Hoses/zgbs/industrial/256335011',

        # # Industrial Food Grade Hoses - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Grade-Hoses/zgbs/industrial/256336011',

        # # Industrial Hydraulic Hoses - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Hoses/zgbs/industrial/256339011',

        # # Industrial Recoiling Hoses - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Recoiling-Hoses/zgbs/industrial/256342011',

        # # Industrial Suction & Vacuum Hoses - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Suction-Vacuum-Hoses/zgbs/industrial/10160469011',

        # # Industrial Water Hoses - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Water-Hoses/zgbs/industrial/256344011',

        # # Pipes - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pipes/zgbs/industrial/3062886011',

        # # Industrial Tubing - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tubing/zgbs/industrial/383597011',

        # # Industrial Glass Tubing - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Glass-Tubing/zgbs/industrial/16414121',

        # # Industrial Metal Tubing - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Metal-Tubing/zgbs/industrial/16414261',

        # # Industrial Plastic Tubing - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plastic-Tubing/zgbs/industrial/16414401',

        # # Industrial Rubber Tubing - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rubber-Tubing/zgbs/industrial/700785011',

        # # Valves - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Valves/zgbs/industrial/383615011',

        # # Ball Valves - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ball-Valves/zgbs/industrial/1265144011',

        # # Check Valves - 25
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Check-Valves/zgbs/industrial/1265146011',

        # # Control Valves - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Control-Valves/zgbs/industrial/1265147011',

        # # Diaphragm Valves - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Diaphragm-Valves/zgbs/industrial/1265151011',

        # # Filter Valves - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Filter-Valves/zgbs/industrial/4650343011',

        # # Float Valves - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Float-Valves/zgbs/industrial/4650344011',

        # # Gate Valves - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Gate-Valves/zgbs/industrial/1265149011',

        # # Needle Valves - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Needle-Valves/zgbs/industrial/4650346011',

        # # Plug Valves - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plug-Valves/zgbs/industrial/4650348011',

        # # Industrial Pressure Regulators - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pressure-Regulators/zgbs/industrial/5739457011',

        # # Relief Valves - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Relief-Valves/zgbs/industrial/4650349011',

        # # Solenoid Valves - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solenoid-Valves/zgbs/industrial/1265148011',

        # # Electronic Components - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Components/zgbs/industrial/306506011',

        # # Circuit Protection Products - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Circuit-Protection-Products/zgbs/industrial/306507011',

        # # Circuit Breakers - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Circuit-Breakers/zgbs/industrial/306508011',

        # # Arc Fault Circuit Breakers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Arc-Fault-Circuit-Breakers/zgbs/industrial/8618821011',

        # # Ground Fault Circuit Interrupters - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ground-Fault-Circuit-Interrupters/zgbs/industrial/6355924011',

        # # Magnetic Circuit Breakers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Magnetic-Circuit-Breakers/zgbs/industrial/6355926011',

        # # Miniature Circuit Breakers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Miniature-Circuit-Breakers/zgbs/industrial/6355927011',

        # # Thermal Circuit Breakers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermal-Circuit-Breakers/zgbs/industrial/6355930011',

        # # Thermal-Magnetic Circuit Breakers - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermal-Magnetic-Circuit-Breakers/zgbs/industrial/6355931011',

        # # Fuses - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuses/zgbs/industrial/306515011',

        # # Blade Fuses - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Blade-Fuses/zgbs/industrial/6355932011',

        # # Cartridge Fuses - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cartridge-Fuses/zgbs/industrial/6355933011'

        # # Fuse Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Accessories/zgbs/industrial/6355934011',

        # # Fuse Blocks & Fuse Holders - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Blocks-Holders/zgbs/industrial/6355935011',

        # # Fuse Blocks - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Blocks/zgbs/industrial/6355936011',

        # # Fuse Holders - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Holders/zgbs/industrial/6355937011',

        # # Fuse Links - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fuse-Links/zgbs/industrial/6355938011',

        # # Plug Fuses - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plug-Fuses/zgbs/industrial/6369376011',

        # # Thermistors - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermistors/zgbs/industrial/306526011',

        # # Electromechanical Products - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electromechanical-Products/zgbs/industrial/306528011',

        # # Electromechanical Controllers - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electromechanical-Controllers/zgbs/industrial/306529011',

        # # Motor Speed Controllers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Motor-Speed-Controllers/zgbs/industrial/306530011',

        # # Process Controllers - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Process-Controllers/zgbs/industrial/306532011',

        # # Thermostat Controllers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thermostat-Controllers/zgbs/industrial/306534011',

        # # Indicator Lights - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indicator-Lights/zgbs/industrial/6374814011',

        # # Electronic Component Motors - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Component-Motors/zgbs/industrial/306577011',

        # # Electric Motors - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Motors/zgbs/industrial/3753381',

        # # Electric Fan Motors - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Fan-Motors/zgbs/industrial/6372405011',

        # # Electric Motor Mounts & Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Motor-Mounts-Accessories/zgbs/industrial/6372407011',

        # # Electric Motor Mounts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Motor-Mounts/zgbs/industrial/6372409011',

        # # Electric Motor Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electric-Motor-Accessories/zgbs/industrial/6372411011',

        # # Electrical Motor Controls - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Motor-Controls/zgbs/industrial/6386345011',

        # # Permanent Magnet Motors - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Permanent-Magnet-Motors/zgbs/industrial/6372402011',

        # # Switches - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Switches/zgbs/industrial/306588011',

        # # Industrial Basic Switches - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Basic-Switches/zgbs/industrial/6355941011',

        # # DIP Switches - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-DIP-Switches/zgbs/industrial/306589011',

        # # Foot Switches - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Foot-Switches/zgbs/industrial/5739468011',

        # # Key Operated Switches - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Key-Operated-Switches/zgbs/industrial/5739466011',

        # # Limit Switches - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Limit-Switches/zgbs/industrial/5739467011',

        # # Pushbutton Switches - 35
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pushbutton-Switches/zgbs/industrial/5739464011',

        # # Toggle Switches - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Toggle-Switches/zgbs/industrial/306596011',

        # # Motion Actuated Switches - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Motion-Actuated-Switches/zgbs/industrial/306562011',

        # # Motor Contactors - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Motor-Contactors/zgbs/industrial/306574011',

        # # Motor Drives - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Motor-Drives/zgbs/industrial/306575011',

        # # Electrical Relays - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Electrical-Relays/zgbs/industrial/306578011',

        # # Coaxial Relays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Coaxial-Relays/zgbs/industrial/306579011',

        # # Current Monitoring Relays - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Current-Monitoring-Relays/zgbs/industrial/306580011',

        # # DIN Mount Relays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-DIN-Mount-Relays/zgbs/industrial/306581011',

        # # Overload Relays - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Overload-Relays/zgbs/industrial/6374818011',

        # # PC Board Relays - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-PC-Board-Relays/zgbs/industrial/306583011',

        # # Phase Monitoring Relays - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Phase-Monitoring-Relays/zgbs/industrial/306584011',

        # # Plug In Relays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plug-Relays/zgbs/industrial/6374819011',

        # # Solid State Relays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solid-State-Relays/zgbs/industrial/6374820011',

        # # Voltage Monitoring Relays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Voltage-Monitoring-Relays/zgbs/industrial/306586011',

        # # Solenoids - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solenoids/zgbs/industrial/306587011',

        



        # # Fasteners - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fasteners/zgbs/industrial/383599011',

        # # Anchors - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Anchors/zgbs/industrial/16409341',

        # # Anchor Bolts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Anchor-Bolts/zgbs/industrial/6809676011',

        # # Concrete Screws - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Concrete-Screws/zgbs/industrial/307023011',

        # # Drive Anchors - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drive-Anchors/zgbs/industrial/16409381',

        # # Drywall Anchors - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drywall-Anchors/zgbs/industrial/6906598011',

        # # Hollow-Wall Anchors - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hollow-Wall-Anchors/zgbs/industrial/16409411',

        # # Sleeve Anchors - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sleeve-Anchors/zgbs/industrial/16409441',

        # # Stud Anchors - 1
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Stud-Anchors/zgbs/industrial/16409451',

        # # T-Anchors - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-T-Anchors/zgbs/industrial/16409461',

        # # Toggle Anchors - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Toggle-Anchors/zgbs/industrial/6906601011',

        # # Wedge Anchors - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wedge-Anchors/zgbs/industrial/16409471',

        # # Collated Hardware Fasteners - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Hardware-Fasteners/zgbs/industrial/552420',

        # # Collated Nails - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Nails/zgbs/industrial/552424',

        # # Collated Brad Nails - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Brad-Nails/zgbs/industrial/552426',

        # # Collated Finish Nails - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Finish-Nails/zgbs/industrial/552428',

        # # Collated Framing Nails - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Framing-Nails/zgbs/industrial/552430',

        # # Collated Pinner Nails - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Pinner-Nails/zgbs/industrial/552432',

        # # Collated Roofing Nails - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Roofing-Nails/zgbs/industrial/552434',

        # # Collated Siding Nails - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Siding-Nails/zgbs/industrial/552436',

        # # Collated Screws - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Collated-Screws/zgbs/industrial/552440',

        # # Powder Actuated Fasteners - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Powder-Actuated-Fasteners/zgbs/industrial/8106324011',

        # # Power Tool Staples - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Tool-Staples/zgbs/industrial/552454',

        # # Hardware Nuts - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hardware-Nuts/zgbs/industrial/16409861',

        # # Acorn Nuts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Acorn-Nuts/zgbs/industrial/16409871',

        # # Allen Nuts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Allen-Nuts/zgbs/industrial/16409881',

        # # Barrel & Binding Nuts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Barrel-Binding-Nuts/zgbs/industrial/16409901',

        # # Coupling Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Coupling-Nuts/zgbs/industrial/16409941',

        # # Eye Nuts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Eye-Nuts/zgbs/industrial/16409951',

        # # Flange Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flange-Nuts/zgbs/industrial/16409961',

        # # Hex & Machine Screw Nuts - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Machine-Screw-Nuts/zgbs/industrial/16409981',

        # # Locknuts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Locknuts/zgbs/industrial/16410001',

        # # Nut Inserts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Nut-Inserts/zgbs/industrial/16410011',

        # # Panel Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Panel-Nuts/zgbs/industrial/307021011',

        # # Push Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Push-Nuts/zgbs/industrial/16410031',

        # # Regulator Inlet Nuts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Regulator-Inlet-Nuts/zgbs/industrial/16410041',

        # # Rivet Nuts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rivet-Nuts/zgbs/industrial/16410051',

        # # T-Nuts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-T-Nuts/zgbs/industrial/16410131',

        # # T-Slot Nuts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slot-Nuts/zgbs/industrial/16410141',

        # # Tamper-Resistant Nuts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tamper-Resistant-Nuts/zgbs/industrial/16410111',

        # # Thumb Nuts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thumb-Nuts/zgbs/industrial/16410121',

        # # Weld Nuts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Weld-Nuts/zgbs/industrial/307022011',

        # # Wing Nuts - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wing-Nuts/zgbs/industrial/16410161',

        # # Hardware Pins - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hardware-Pins/zgbs/industrial/16410171',

        # # Clevis Pins - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Clevis-Pins/zgbs/industrial/16410201',

        # # Cotter Pins - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cotter-Pins/zgbs/industrial/16410221',

        # # Dowel Pins - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Dowel-Pins/zgbs/industrial/16410231',

        # # Locking Pins - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Locking-Pins/zgbs/industrial/6906604011',

        # # Hitch Pins - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hitch-Pins/zgbs/industrial/16410311',

        # # Quick-Release Pins - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Quick-Release-Pins/zgbs/industrial/16410371',

        # # Spring Pins - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spring-Pins/zgbs/industrial/16410401',

        # # Retaining Rings - 8
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Retaining-Rings/zgbs/industrial/16410451',

        # # Rivets - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rivets/zgbs/industrial/16410461',

        # # Blind Rivets - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Blind-Rivets/zgbs/industrial/16410471',

        # # Solid Rivets - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solid-Rivets/zgbs/industrial/16410491',

        # # Tubular Rivets - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tubular-Rivets/zgbs/industrial/16410511',

        # # Rivet-Type Studs - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rivet-Type-Studs/zgbs/industrial/16410791',

        # # Rivet Washers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rivet-Washers/zgbs/industrial/16410911',

        # # Screws - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Screws/zgbs/industrial/16403521',

        # # Hex Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Bolts/zgbs/industrial/16409601',

        # # Captive Screws - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Captive-Screws/zgbs/industrial/16410541',

        # # Carriage Bolts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Carriage-Bolts/zgbs/industrial/16409521',

        # # Hanger Bolts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hanger-Bolts/zgbs/industrial/16409591',

        # # Drywall Screws - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drywall-Screws/zgbs/industrial/16410561',

        # # Expansion Bolts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Expansion-Bolts/zgbs/industrial/16409561',

        # # Eyebolts - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Eyebolts/zgbs/industrial/16409571',

        # # Lag Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lag-Bolts/zgbs/industrial/16409621',

        # # Machine Screws - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Machine-Screws/zgbs/industrial/16403531',

        # # Panel Screws - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Panel-Screws/zgbs/industrial/16410571',

        # # Penta Head Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Penta-Head-Bolts/zgbs/industrial/16409631',

        # # Plow Bolts - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plow-Bolts/zgbs/industrial/16409641',

        # # Self-drilling Screws - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Self-drilling-Screws/zgbs/industrial/307025011',

        # # Set Screws - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Set-Screws/zgbs/industrial/16410581',

        # # Sheet Metal Screws - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sheet-Metal-Screws/zgbs/industrial/16410591',

        # # Shoulder Screws - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Shoulder-Screws/zgbs/industrial/16410601',

        # # Socket Cap Screws - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Socket-Cap-Screws/zgbs/industrial/16410531',

        # # Square Head Bolts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Square-Head-Bolts/zgbs/industrial/16409661',

        # # Structural Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Structural-Bolts/zgbs/industrial/16409691',

        # # T-Slot Bolts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slot-Bolts/zgbs/industrial/16409741',

        # # Tension Control Bolts - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tension-Control-Bolts/zgbs/industrial/16409711',

        # # Thumb Screws - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thumb-Screws/zgbs/industrial/16410621',

        # # Toggle Bolts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Toggle-Bolts/zgbs/industrial/16409731',

        # # U-Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-U-Bolts/zgbs/industrial/16409751',

        # # Wheel Bolts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wheel-Bolts/zgbs/industrial/16409761',

        # # Wood Screws - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wood-Screws/zgbs/industrial/16410631',

        # # Spacers & Standoffs - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spacers-Standoffs/zgbs/industrial/16413321',

        # # Hardware Spacers - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hardware-Spacers/zgbs/industrial/6909200011',

        # # Standoffs - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Standoffs/zgbs/industrial/6909196011',

        # # Threaded Inserts - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threaded-Inserts/zgbs/industrial/16410701',

        # # Helical Threaded Inserts - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Helical-Threaded-Inserts/zgbs/industrial/6909192011',

        # # Externally Threaded Inserts - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Externally-Threaded-Inserts/zgbs/industrial/6909193011',

        # # Threaded Rods & Studs - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threaded-Rods-Studs/zgbs/industrial/16410711',

        # # Equal Thread Length Rods & Studs - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Equal-Thread-Length-Rods-Studs/zgbs/industrial/16410721',

        # # Fully Threaded Rods & Studs - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Fully-Threaded-Rods-Studs/zgbs/industrial/16410731',

        # # Hardware Washers - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hardware-Washers/zgbs/industrial/16410821',

        # # Belleville Washers - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Belleville-Washers/zgbs/industrial/16410831',

        # # Beveled Washers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Beveled-Washers/zgbs/industrial/16410841',

        # # Cup Washers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cup-Washers/zgbs/industrial/323585011',

        # # Flat Washers - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flat-Washers/zgbs/industrial/16410891',

        # # Lock Washers - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lock-Washers/zgbs/industrial/16410901',

        # # Retaining Washers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Retaining-Washers/zgbs/industrial/323586011',

        # # Sealing Washers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sealing-Washers/zgbs/industrial/16410921',

        # # Hardware Shoulder Washers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hardware-Shoulder-Washers/zgbs/industrial/2526654011',

        # # Slotted Washers - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slotted-Washers/zgbs/industrial/16410931',

        # # Wave Washers & Wave Springs - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wave-Washers-Springs/zgbs/industrial/16410981',

        # # Filtration - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Filtration/zgbs/industrial/3061625011',

        # # Compressed Air Filtration - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Filtration/zgbs/industrial/3419728011',

        # # Compressed Air Dryers, Separators & Drains - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Dryers-Separators-Drains/zgbs/industrial/3419729011',

        # # Compressed Air Separators - 7
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Separators/zgbs/industrial/3419730011',

        # # Compressed Air Drains - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Drains/zgbs/industrial/3419731011',

        # # Compressed Air Filters - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Filters/zgbs/industrial/3419732011',

        # # Compressed Air Filters, Regulators & Lubricators - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Filters-Regulators-Lubricators/zgbs/industrial/3419736011',

        # # Compressed Air Combination Filter Regulators - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Combination-Filter-Regulators/zgbs/industrial/3419737011',

        # # Compressed Air Combination Filter Regulator Lubricators - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Combination-Filter-Regulator-Lubricators/zgbs/industrial/3419738011',

        # # Compressed Air Lubricators - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Lubricators/zgbs/industrial/3419739011',

        # # Compressed Air Regulators - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Regulators/zgbs/industrial/3419740011',

        # # Compressed Air Pneumatic Mufflers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Compressed-Air-Pneumatic-Mufflers/zgbs/industrial/3419741011',

        # # Furnace Filters - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Furnace-Filters/zgbs/industrial/13399891',

        # # Hydraulic Filtration - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulic-Filtration/zgbs/industrial/3419746011',

        # # Industrial Process Filtration - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Process-Filtration/zgbs/industrial/3419742011',

        # # Industrial Process Filter Bags - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Process-Filter-Bags/zgbs/industrial/3419743011',

        # # Industrial Process Filter Cartridges - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Process-Filter-Cartridges/zgbs/industrial/3419744011',

        # # Industrial Process Filter Housings - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Process-Filter-Housings/zgbs/industrial/3419745011',

        # # Lab Filters - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Lab-Filters/zgbs/industrial/318079011',

        # # Air Sampling Lab Filters - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Air-Sampling-Lab-Filters/zgbs/industrial/393363011',

        # # Bottletop Lab Filters - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bottletop-Lab-Filters/zgbs/industrial/318080011',

        # # Glass Fiber Lab Filters - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Glass-Fiber-Lab-Filters/zgbs/industrial/393367011',

        # # Inline Lab Filters - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Inline-Lab-Filters/zgbs/industrial/393364011',

        # # Qualitative Lab Filter Paper - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Qualitative-Lab-Filter-Paper/zgbs/industrial/393368011',

        # # Quantitative Lab Filter Paper - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Quantitative-Lab-Filter-Paper/zgbs/industrial/393369011',

        # # Syringe Lab Filters - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Syringe-Lab-Filters/zgbs/industrial/318082011',

        # # Industrial Plumbing Strainers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plumbing-Strainers/zgbs/industrial/5760169011',

        # # Industrial Plumbing Basket Strainers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plumbing-Basket-Strainers/zgbs/industrial/5760173011',

        # # Industrial Plumbing Suction Strainers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plumbing-Suction-Strainers/zgbs/industrial/5760174011',

        # # Industrial Plumbing T Strainers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plumbing-Strainers/zgbs/industrial/5760171011',

        # # Industrial Plumbing Y Strainers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Plumbing-Strainers/zgbs/industrial/5760170011',

        # # Industrial Water Purification - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Water-Purification/zgbs/industrial/3419750011',

        # # Faucet Mount Water Filters - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Faucet-Mount-Water-Filters/zgbs/industrial/680337011',

        # # Under-Sink Water Filters - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Under-Sink-Water-Filters/zgbs/industrial/13397611',

        # # Replacement Water Filters - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Replacement-Water-Filters/zgbs/industrial/3741111',

        # # Replacement Countertop Water Filters - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Replacement-Countertop-Water-Filters/zgbs/industrial/3741141',

        # # Replacement Faucet Water Filters - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Replacement-Faucet-Water-Filters/zgbs/industrial/3741131',

        # # Replacement Pitcher Water Filters - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Replacement-Pitcher-Water-Filters/zgbs/industrial/3741121',

        # # Replacement Under-Sink Water Filters - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Replacement-Under-Sink-Water-Filters/zgbs/industrial/3741151',

        # # Food Service Equipment & Supplies - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Equipment-Supplies/zgbs/industrial/6054382011',

        # # Commercial Espresso Machines & Coffee Makers - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Espresso-Machines-Coffee-Makers/zgbs/industrial/5315101011',

        # # Commercial Food Storage - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Storage/zgbs/industrial/9768325011',

        # # Commercial Food Pans - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Pans/zgbs/industrial/5298284011',

        # # Commercial Food Scoops - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Scoops/zgbs/industrial/5298291011',

        # # Commercial Food Storage Container Lids - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Storage-Container-Lids/zgbs/industrial/5298293011',

        # # Commercial Restaurant Sinks - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Restaurant-Sinks/zgbs/industrial/5315090011',

        # # Concession & Vending Equipment - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Concession-Vending-Equipment/zgbs/industrial/5315091011',

        # # Commercial Cooking Equipment - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Cooking-Equipment/zgbs/industrial/6054385011',

        # # Commercial Broilers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Broilers/zgbs/industrial/5315077011',

        # # Cooking Equipment Accessories - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cooking-Equipment-Accessories/zgbs/industrial/6054847011',

        # # Commercial Dishwashing Equipment - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Dishwashing-Equipment/zgbs/industrial/5315092011',

        # # Commercial Dish Racks - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Dish-Racks/zgbs/industrial/5315094011',

        # # Commercial Dishwashers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Dishwashers/zgbs/industrial/5315095011',

        # # Food Service Display Products - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Display-Products/zgbs/industrial/5298059011',

        # # Food Service Displayware - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Displayware/zgbs/industrial/5298060011',

        # # Food Service Display Risers - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Display-Risers/zgbs/industrial/5298065011',

        # # Food Service Display Trays - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Display-Trays/zgbs/industrial/5298067011',

        # # Commercial Food Merchandisers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Merchandisers/zgbs/industrial/5315122011',

        # # Food Service Signage - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Signage/zgbs/industrial/5298068011',

        # # Food Service Outdoor Signs - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Outdoor-Signs/zgbs/industrial/5298069011',

        # # Food Service Symbol Signs - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Symbol-Signs/zgbs/industrial/5298072011',

        # # Food Service Tabletop Signs - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Tabletop-Signs/zgbs/industrial/5298073011',

        # # Food Service Disposables - 90
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Disposables/zgbs/industrial/6134197011',

        # # Disposable Apparel - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Apparel/zgbs/industrial/5016430011',

        # # Disposable Safety Gloves - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Safety-Gloves/zgbs/industrial/4954444011',

        # # Non-Sterile Disposable Safety Gloves - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Non-Sterile-Disposable-Safety-Gloves/zgbs/industrial/7491821011',

        # # Sterile Disposable Safety Gloves - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sterile-Disposable-Safety-Gloves/zgbs/industrial/393304011',

        # # Sanitary Masks - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanitary-Masks/zgbs/industrial/6125377011',

        # # Food Service Butcher & Freezer Paper - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Butcher-Freezer-Paper/zgbs/industrial/8794573011',

        # # Disposable Cookware - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Cookware/zgbs/industrial/6054383011',

        # # Cups & Straws - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cups-Straws/zgbs/industrial/15343011',

        # # Disposable Cups - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Cups/zgbs/industrial/15757581',

        # # Disposable Stemware - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Stemware/zgbs/industrial/15754791',

        # # Disposable Drinking Straws - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Drinking-Straws/zgbs/industrial/15754801',

        # # Paper Napkins - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Paper-Napkins/zgbs/industrial/15347411',

        # # Paper Towels - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Paper-Towels/zgbs/industrial/15347401',

        # # Disposable Plates & Cutlery - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Plates-Cutlery/zgbs/industrial/15342991',

        # # Disposable Bowls - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Bowls/zgbs/industrial/15757561',

        # # Disposable Forks - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Forks/zgbs/industrial/15757571',

        # # Disposable Knives - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Knives/zgbs/industrial/15750761',

        # # Paper & Plastic Plates - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Paper-Plastic-Plates/zgbs/industrial/15750751',

        # # Disposable Spoons - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Spoons/zgbs/industrial/15754771',

        # # Disposable Sporks - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Sporks/zgbs/industrial/15754781',

        # # Disposable Table Covers - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Table-Covers/zgbs/industrial/6054384011',

        # # Disposable Doilies - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Doilies/zgbs/industrial/5016461011',

        # # Disposable Table Skirts - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Table-Skirts/zgbs/industrial/5016463011',

        # # Take Out Containers - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Take-Out-Containers/zgbs/industrial/5016465011',

        # # Bakery Take Out Containers - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bakery-Take-Out-Containers/zgbs/industrial/5016466011',

        # # Disposable Cake & Pizza Circles - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Cake-Pizza-Circles/zgbs/industrial/8794579011',

        # # Clamshell Take Out Containers - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Clamshell-Take-Out-Containers/zgbs/industrial/5016472011',

        # # Pizza Boxes - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pizza-Boxes/zgbs/industrial/5016474011',

        # # Disposable Souffle Cups - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Disposable-Souffle-Cups/zgbs/industrial/5016475011',

        # # Commercial Food & Dish Transport - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Dish-Transport/zgbs/industrial/5298299011',

        # # Commercial Food Preparation Equipment - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Preparation-Equipment/zgbs/industrial/6054386011',

        # # Commercial Fry Baggers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Fry-Baggers/zgbs/industrial/6054851011',

        # # Commercial Mixing Paddles - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Mixing-Paddles/zgbs/industrial/5298143011',

        # # Commercial Food Warmers - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Food-Warmers/zgbs/industrial/5315121011',

        # # Menu & Check Displayers - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Menu-Check-Displayers/zgbs/industrial/6054395011',

        # # Commercial Check Presenters - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Check-Presenters/zgbs/industrial/5314720011',

        # # Commercial Guest Checks - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Guest-Checks/zgbs/industrial/8794572011',

        # # Commercial Menu Holders - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Menu-Holders/zgbs/industrial/5314721011',

        # # Commercial Refrigeration Equipment - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Refrigeration-Equipment/zgbs/industrial/6054387011',

        # # Restaurant Furniture - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Restaurant-Furniture/zgbs/industrial/6054389011',

        # # Food Service Shelves & Racks - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Shelves-Racks/zgbs/industrial/6054392011',

        # # Food Service Storage Rack Accessories - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Storage-Rack-Accessories/zgbs/industrial/5298319011',

        # # Food Service Storage Rack Shelves - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Storage-Rack-Shelves/zgbs/industrial/5298320011',

        # # Commercial Worktables and Workstations - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Worktables-Workstations/zgbs/industrial/5315132011',




        # # Industrial & Scientific - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial',

        # # Abrasive & Finishing Products - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Products/zgbs/industrial/256167011',

        # # Abrasive Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Accessories/zgbs/industrial/401506011',

        # # Abrasive Dressing Tools - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Dressing-Tools/zgbs/industrial/256180011',

        # # Abrasive Mandrels - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Mandrels/zgbs/industrial/401510011',

        # # Abrasive Wheel Adapters & Flanges - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheel-Adapters-Flanges/zgbs/industrial/2734041011',

        # # Tool Holders - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tool-Holders/zgbs/industrial/401549011',

        # # Industrial Sander Belts - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sander-Belts/zgbs/industrial/3442587011',

        # # Abrasive Brushes - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Brushes/zgbs/industrial/256168011',

        # # Power Sander Bristle Discs - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Bristle-Discs/zgbs/industrial/310357011',

        # # Abrasive Power Brushes - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Power-Brushes/zgbs/industrial/2665577011',

        # # Abrasive Cup Power Brushes - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cup-Power-Brushes/zgbs/industrial/2665578011',

        # # Abrasive Flat End Power Brushes - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Flat-End-Power-Brushes/zgbs/industrial/2665579011',

        # # Abrasive Spiral Power Brushes - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Spiral-Power-Brushes/zgbs/industrial/2665580011',

        # # Abrasive Wheel Power Brushes - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheel-Power-Brushes/zgbs/industrial/2665581011',

        # # Scratch Brushes - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Scratch-Brushes/zgbs/industrial/1265107011',

        # # Abrasive Mounted Points - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Mounted-Points/zgbs/industrial/401518011',

        # # Abrasive Bands - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Bands/zgbs/industrial/401505011',

        # # Abrasive Cartridge Rolls - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cartridge-Rolls/zgbs/industrial/256169011',

        # # Power Sanding Sleeves - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sanding-Sleeves/zgbs/industrial/552596',

        # # Abrasive Grinding Cones & Plugs - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Cones-Plugs/zgbs/industrial/2734046011',

        # # Abrasive Grinding Mounted Points - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Mounted-Points/zgbs/industrial/2734045011',

        # # Abrasive Wheels & Discs - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Wheels-Discs/zgbs/industrial/2665570011',

        # # Angle & Die Grinder Wheels - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Angle-Die-Grinder-Wheels/zgbs/industrial/2665571011',

        # # Bench & Pedestal Grinding Wheels - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bench-Pedestal-Grinding-Wheels/zgbs/industrial/256204011',

        # # Abrasive Cutoff Wheels - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Cutoff-Wheels/zgbs/industrial/256194011',

        # # Power Sander Flap Discs - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Flap-Discs/zgbs/industrial/256175011',

        # # Abrasive Flap Wheels - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Flap-Wheels/zgbs/industrial/256200011',

        # # Abrasive Grinding Discs - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Grinding-Discs/zgbs/industrial/2665574011',

        # # Abrasive OD Grinding Wheels - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-OD-Grinding-Wheels/zgbs/industrial/2665575011',

        # # Power Oscillating Tool Sanding Pads - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Oscillating-Tool-Sanding-Pads/zgbs/industrial/8106528011',

        # # Abrasive Sanding Disc Backing Pads - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Sanding-Disc-Backing-Pads/zgbs/industrial/2665576011',

        # # Power Sanding Discs - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sanding-Discs/zgbs/industrial/552588',

        # # Power Sander Fiber Backed Abrasive Discs - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Fiber-Backed-Abrasive-Discs/zgbs/industrial/256176011',

        # # Power Sander Hook & Loop Discs - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Hook-Loop-Discs/zgbs/industrial/256177011',

        # # Power Sander PSA Discs - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-PSA-Discs/zgbs/industrial/256178011',

        # # Power Sander Quick Change Discs - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sander-Quick-Change-Discs/zgbs/industrial/256179011',

        # # Surface Grinding Wheels - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Surface-Grinding-Wheels/zgbs/industrial/256207011',

        # # Abrasive Tool Room Grinding Wheels - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Tool-Room-Grinding-Wheels/zgbs/industrial/256202011',

        # # Unitized & Convolute Wheels - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Unitized-Convolute-Wheels/zgbs/industrial/256203011',

        # # Abrasive Finishing Products - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Products/zgbs/industrial/2734049011'

        # # Buffing & Polishing Accessories - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Polishing-Accessories/zgbs/industrial/256209011',

        # # Buffing & Polishing Mounted Points - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Polishing-Mounted-Points/zgbs/industrial/979146011',

        # # Buffing Kits - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Kits/zgbs/industrial/256211011',

        # # Buffing Wheels - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Buffing-Wheels/zgbs/industrial/256214011',

        # # Felt Bobs - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Felt-Bobs/zgbs/industrial/256215011',

        # # Abrasive Finishing Compounds - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Compounds/zgbs/industrial/2734050011',

        # # Laps & Hones - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Laps-Hones/zgbs/industrial/256182011',

        # # Flex Hones - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Flex-Hones/zgbs/industrial/256184011',

        # # Honing Stones - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Honing-Stones/zgbs/industrial/256185011',

        # # Tumbling Media - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tumbling-Media/zgbs/industrial/256192011',

        # # Hand Files - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Files/zgbs/industrial/256181011',

        # # Manual Sanding Products - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Manual-Sanding-Products/zgbs/industrial/2734051011',

        # # Sanding Blocks - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Blocks/zgbs/industrial/553332',

        # # Sanding Pads - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Pads/zgbs/industrial/2734054011',

        # # Sanding Rolls - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Rolls/zgbs/industrial/401511011',

        # # Sanding Sheets - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Sheets/zgbs/industrial/256189011',

        # # Sanding Sponges - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Sponges/zgbs/industrial/2734053011',

        # # Sanding Tapes - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Tapes/zgbs/industrial/401512011',

        # # Sanding Steel Wool - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sanding-Steel-Wool/zgbs/industrial/2734052011',

        # # Power Sand Blasters - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Sand-Blasters/zgbs/industrial/552714',

        # # Sharpening Stones - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sharpening-Stones/zgbs/industrial/553346',

        # # Additive Manufacturing Products - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Additive-Manufacturing-Products/zgbs/industrial/6066126011',

        # # 3D Printers - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printers/zgbs/industrial/6066127011',

        # # 3D Printing Supplies - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printing-Supplies/zgbs/industrial/6066128011',

        # # 3D Printer Parts & Accessories - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Parts-Accessories/zgbs/industrial/6066132011',

        # # 3D Printer Extruders - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Extruders/zgbs/industrial/8481415011',

        # # 3D Printer Platforms - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Platforms/zgbs/industrial/8481418011',

        # # 3D Printer Motors - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Motors/zgbs/industrial/8481417011',

        # # 3D Printer Interface & Driver Modules - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Interface-Driver-Modules/zgbs/industrial/8481416011',

        # # 3D Printer Controllers - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Controllers/zgbs/industrial/8481414011',

        # # 3D Printer Accessories - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-3D-Printer-Accessories/zgbs/industrial/8481419011',

        # # Commercial Door Products - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Products/zgbs/industrial/10773802011',

        # # Commercial Access Control - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Control/zgbs/industrial/10773803011',

        # # Commercial Access Cards & Card Readers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Cards-Card-Readers/zgbs/industrial/10773804011',

        # # Commercial Door Control - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Control/zgbs/industrial/10773848011',

        # # Commercial Access Door Control - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Access-Door-Control/zgbs/industrial/10773853011',

        # # Security Access-Control Keypads - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Security-Access-Control-Keypads/zgbs/industrial/11041131',

        # # Commercial Electromagnetic Locks - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Electromagnetic-Locks/zgbs/industrial/10773876011',

        # # Commercial Door Hardware - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Hardware/zgbs/industrial/10773891011',

        # # Commercial Door Guards - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Guards/zgbs/industrial/10773913011',

        # # Commercial Door Hinges - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Hinges/zgbs/industrial/10773915011',

        # # Commercial Door Stops - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Stops/zgbs/industrial/10773917011',

        # # Commercial Exit Devices - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Exit-Devices/zgbs/industrial/10773918011',

        # # Commercial Push & Pull Locksets & Handles - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Push-Pull-Locksets-Handles/zgbs/industrial/10773952011',

        # # Sliding Door Hardware - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Sliding-Door-Hardware/zgbs/industrial/9628854011',

        # # Cutting Tools - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Tools/zgbs/industrial/383598011',

        # # Band Saw Blades - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Band-Saw-Blades/zgbs/industrial/552288',

        # # Broaches - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Broaches/zgbs/industrial/340030011',

        # # Cutting Burs - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Burs/zgbs/industrial/256263011',

        # # Cutting Tool Coolants - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Tool-Coolants/zgbs/industrial/401548011',

        # # Deburring Cutters - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Deburring-Cutters/zgbs/industrial/340035011',

        # # Drill & Tap Sets - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drill-Tap-Sets/zgbs/industrial/8906585011',

        # # Hole Saws & Accessories - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saws-Accessories/zgbs/industrial/552402',

        # # Hole Saw Arbors - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saw-Arbors/zgbs/industrial/8106327011',

        # # Hole Saw Sets & Kits - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saw-Sets-Kits/zgbs/industrial/8106328011',

        # # Hole Saws - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Saws/zgbs/industrial/256292011',

        # # Indexable Insert Holders - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Insert-Holders/zgbs/industrial/257513011',

        # # Drilling Holders - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drilling-Holders/zgbs/industrial/257515011',

        # # Face Mill Holders - 1
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Face-Mill-Holders/zgbs/industrial/262582011',

        # # Indexable Inserts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Inserts/zgbs/industrial/257519011',

        # # Turning Inserts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Turning-Inserts/zgbs/industrial/257522011',

        # # Industrial Drill Bits - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drill-Bits/zgbs/industrial/256264011',

        # # Combination Drill & Taps - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Combination-Drill-Taps/zgbs/industrial/6001488011',

        # # Masonry Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Masonry-Drill-Bits/zgbs/industrial/256276011',

        # # Core Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Core-Drill-Bits/zgbs/industrial/256268011',

        # # Masonry Drill Bit Sets - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Masonry-Drill-Bit-Sets/zgbs/industrial/8906589011',

        # # Rotary Hammer Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Rotary-Hammer-Drill-Bits/zgbs/industrial/8906591011',

        # # Metalworking & Multipurpose Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Metalworking-Multipurpose-Drill-Bits/zgbs/industrial/2941336011',

        # # Annular Cutters - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Annular-Cutters/zgbs/industrial/340028011',

        # # Circuit Board Drill Bits - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Circuit-Board-Drill-Bits/zgbs/industrial/401551011',

        # # Industrial Indexable Inserts - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Indexable-Inserts/zgbs/industrial/8906583011',

        # # Metalworking & Multipurpose Drill Sets - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Metalworking-Multipurpose-Drill-Sets/zgbs/industrial/8906587011',

        # # Reduced Shank Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Reduced-Shank-Drill-Bits/zgbs/industrial/340052011',

        # # Step Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Step-Drill-Bits/zgbs/industrial/256287011',

        # # Subland Drill Bits - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Subland-Drill-Bits/zgbs/industrial/2941338011',

        # # Twist Drill Bits - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Twist-Drill-Bits/zgbs/industrial/552416',

        # # Extra Long Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Extra-Long-Drill-Bits/zgbs/industrial/256270011',

        # # Hex-Shank Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Shank-Drill-Bits/zgbs/industrial/552400',

        # # Jobber Drill Bits - 80
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Jobber-Drill-Bits/zgbs/industrial/256275011',

        # # Long Length Drill Bits - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Long-Length-Drill-Bits/zgbs/industrial/256289011',

        # # Mechanic's Length Drill Bits - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Mechanics-Length-Drill-Bits/zgbs/industrial/2941341011',

        # # Short Length Drill Bits - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Short-Length-Drill-Bits/zgbs/industrial/2941342011',

        # # Wood Drill Bit Sets - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wood-Drill-Bit-Sets/zgbs/industrial/8906593011',

        # # Wood Drill Bits - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Wood-Drill-Bits/zgbs/industrial/256291011',

        # # Auger Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Auger-Drill-Bits/zgbs/industrial/552410',

        # # Boring Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Boring-Drill-Bits/zgbs/industrial/552392',

        # # Brad-Point Drill Bits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Brad-Point-Drill-Bits/zgbs/industrial/552394',

        # # Forstner Drill Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Forstner-Drill-Bits/zgbs/industrial/552398',

        # # Self-Feed Drill Bits - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Self-Feed-Drill-Bits/zgbs/industrial/552408',

        # # Spade Drill Bits - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spade-Drill-Bits/zgbs/industrial/552412',

        # # Countersink Drill Bits - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Countersink-Drill-Bits/zgbs/industrial/552396',

        # # Milling Tools - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Milling-Tools/zgbs/industrial/5825198011',

        # # End Mills - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-End-Mills/zgbs/industrial/256305011',

        # # Ball Nose End Mills - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Ball-Nose-End-Mills/zgbs/industrial/340044011',

        # # Square Nose End Mills - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Square-Nose-End-Mills/zgbs/industrial/2382225011',

        # # Tapered End Mills - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Tapered-End-Mills/zgbs/industrial/340047011',

        # # Hand Punches - 60
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Punches/zgbs/industrial/2225051011',

        # # Arch Punches - 15
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Arch-Punches/zgbs/industrial/2225054011',

        # # Center Punches - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Center-Punches/zgbs/industrial/2225055011',

        # # Drift Punches - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Drift-Punches/zgbs/industrial/2225056011',

        # # Hole Punches - 40
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hole-Punches/zgbs/industrial/2225057011',

        # # Knockout Punches - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Knockout-Punches/zgbs/industrial/2225058011',

        # # Pin Punches - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pin-Punches/zgbs/industrial/2225059011',

        # # Transfer Punches - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Transfer-Punches/zgbs/industrial/2225060011',

        # # Bridge & Construction Reamers - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Bridge-Construction-Reamers/zgbs/industrial/2611570011',

        # # Hand Reamers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hand-Reamers/zgbs/industrial/256298011',

        # # Taper Pin Reamers - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Taper-Pin-Reamers/zgbs/industrial/256300011',

        # # Taper Pipe Reamers - 2
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Taper-Pipe-Reamers/zgbs/industrial/2611571011',

        # # Router Bits - 70
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Bits/zgbs/industrial/3116511',

        # # Router Bearings & Bit-Repair Parts - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Bearings-Bit-Repair-Parts/zgbs/industrial/3116521',

        # # Router Door & Window Bits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Router-Door-Window-Bits/zgbs/industrial/3116531',

        # # Edge Treatment & Grooving Router Bits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Edge-Treatment-Grooving-Router-Bits/zgbs/industrial/3116541',

        # # Joinery Router Bits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Joinery-Router-Bits/zgbs/industrial/3116551',

        # # Solid Surface Router Bits - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Solid-Surface-Router-Bits/zgbs/industrial/3116561',

        # # Straight, Spiral & Trim Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Spiral-Trim-Bits/zgbs/industrial/3116571',

        # # Spiral Router Bits - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Spiral-Router-Bits/zgbs/industrial/686958011',

        # # Straight Router Bits - 50
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Router-Bits/zgbs/industrial/686957011',

        # # Trim Router Bits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Trim-Router-Bits/zgbs/industrial/686959011',

        # # Slotting Cutters - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slotting-Cutters/zgbs/industrial/256311011',

        # # Slotting Cutter Arbors - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Slotting-Cutter-Arbors/zgbs/industrial/256313011',

        # # Three Wing Slotting Cutters - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Three-Wing-Slotting-Cutters/zgbs/industrial/256314011',

        # # Thread Repair Kits - 30
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Repair-Kits/zgbs/industrial/15709071',

        # # Thread Metric Inserts & Repair Kits - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Metric-Inserts-Repair-Kits/zgbs/industrial/15709091',

        # # Thread Spark Plug Thread Repair Kits - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Spark-Plug-Repair-Kits/zgbs/industrial/15709101',

        # # Threading Dies - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threading-Dies/zgbs/industrial/256320011',

        # # Hex Threading Dies - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Hex-Threading-Dies/zgbs/industrial/256321011',

        # # Round Threading Dies - 3
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Round-Threading-Dies/zgbs/industrial/256322011',

        # # Threading Taps - 20
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Threading-Taps/zgbs/industrial/256324011',

        # # Pipe Taps - 10
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Pipe-Taps/zgbs/industrial/340041011',

        # # Straight Flute Taps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Straight-Flute-Taps/zgbs/industrial/256326011',

        # # Thread Milling Taps - 5
        # 'http://www.amazon.com/Best-Sellers-Industrial-Scientific-Thread-Milling-Taps/zgbs/industrial/340043011',




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
