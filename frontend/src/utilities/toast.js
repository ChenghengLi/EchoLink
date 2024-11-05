
// Toast mixin for Swal.

import Swal from 'sweetalert2'

const Toast = Swal.mixin({
    toast: true,
    position: 'top',
    iconColor: 'white',
    customClass: {
        popup: 'colored-toast',
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: false,
})

export default Toast