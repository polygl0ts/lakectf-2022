# How to not turn crazy (QEMU PTSD anyone?)

1. `docker compose build`
2. `docker compose up`
3. Connect to the challenge with `nc localhost 3700`, ssh into the arm64 VM
   with `ssh root@localhost -p 30022`

Note: The challenge is located in `/app` in the VM. The VM contains exactly the
`paccheri` and `libc.so.6` you're provided with. The only difference is that in
the VM, `/proc/self/maps` is symlinked to `/app/postal_codes` -- we unfortunately
cannot ship symlinks ;)
