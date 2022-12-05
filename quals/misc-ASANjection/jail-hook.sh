#!/bin/sh
cat <<EOF >> $nsjail_cfg
mount {
    src: "/proc"
    dst: "/proc"
    is_bind: true
    rw: false
}
EOF
