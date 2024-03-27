clear -all
check_spv -init

# Set up the design
####################################################################################################
#  This file needs to:
#  - Analyze (i.e. parse) the design
#  - Elaborate (i.e. compile) the design
#  - Set the Clock and Resets to the design
source ./jg_setup.tcl

# OTP Key Property
####################################################################################################
foreach output [get_design_info -list output] {
    check_spv -create -name otp_key_${output}_precond0 -from key -to $output -to_precond pprot\[2\]==0
    check_spv -create -name otp_key_${output}_precond1 -from key -to $output -to_precond pprot\[1\]==0
}

# OTP Key Integrity Property
####################################################################################################
check_spv -create -name otp_key_pwdata_precond0 -from pwdata -to key -to_precond pprot\[0\]==0

# OTP Plaintext Property
####################################################################################################
foreach output [get_design_info -list output] {
    check_spv -create -name otp_plaintext_${output} -from data -to $output
}

check_spv -prove