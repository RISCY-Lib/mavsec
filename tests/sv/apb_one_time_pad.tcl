clear -all
check_spv -init

analyze -sv test_modules/apb_one_time_pad.sv
elaborate -top apb_one_time_pad

clock pclk
reset ~preset_n

foreach output [get_design_info -list output] {
    check_spv -create -name key_to_${output}_instr -from key -to $output -to_precond pprot\[2\]
    check_spv -create -name key_to_${output}_insecure -from key -to $output -to_precond pprot\[1\]
}
check_spv -prove