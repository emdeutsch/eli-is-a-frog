#!/bin/bash

#═══════════════════════════════════════════════════════════════════════════════
#  ███████╗██╗     ██╗    ██╗███████╗     █████╗     ███████╗██████╗  ██████╗  ██████╗
#  ██╔════╝██║     ██║    ██║██╔════╝    ██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗██╔════╝
#  █████╗  ██║     ██║    ██║███████╗    ███████║    █████╗  ██████╔╝██║   ██║██║  ███╗
#  ██╔══╝  ██║     ██║    ██║╚════██║    ██╔══██║    ██╔══╝  ██╔══██╗██║   ██║██║   ██║
#  ███████╗███████╗██║    ██║███████║    ██║  ██║    ██║     ██║  ██║╚██████╔╝╚██████╔╝
#  ╚══════╝╚══════╝╚═╝    ╚═╝╚══════╝    ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝
#
#  THE ULTIMATE CINEMATIC EXPERIENCE - DIRECTOR'S CUT EXTENDED EDITION
#  Runtime: Until you press Ctrl+C or your terminal explodes
#  Budget: $0 but priceless in spirit
#═══════════════════════════════════════════════════════════════════════════════

# Terminal dimensions
TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

# Color definitions - compatible with bash 3.2
C_BLACK='\033[0;30m'
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'
C_MAGENTA='\033[0;35m'
C_CYAN='\033[0;36m'
C_WHITE='\033[0;37m'
C_BRIGHT_BLACK='\033[1;30m'
C_BRIGHT_RED='\033[1;31m'
C_BRIGHT_GREEN='\033[1;32m'
C_BRIGHT_YELLOW='\033[1;33m'
C_BRIGHT_BLUE='\033[1;34m'
C_BRIGHT_MAGENTA='\033[1;35m'
C_BRIGHT_CYAN='\033[1;36m'
C_BRIGHT_WHITE='\033[1;37m'
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_DIM='\033[2m'
C_BLINK='\033[5m'
C_REVERSE='\033[7m'

# Extended 256 colors
color256() {
    echo -e "\033[38;5;${1}m"
}

bg256() {
    echo -e "\033[48;5;${1}m"
}

# RGB colors (if terminal supports)
rgb() {
    echo -e "\033[38;2;${1};${2};${3}m"
}

bg_rgb() {
    echo -e "\033[48;2;${1};${2};${3}m"
}

NC='\033[0m'

# Game state - using regular variables for bash 3.2 compatibility
ELI_X=40
ELI_Y=15
FLIES_EATEN=0
HEALTH=100
LEVEL=1
SCORE=0
COMBO=0
MAX_COMBO=0
BOSS_HEALTH=100
TIME_OF_DAY="day"
WEATHER="clear"
CURRENT_SCENE=0
TOTAL_RIBBITS=0

# Particle system
declare -a PARTICLES_X
declare -a PARTICLES_Y
declare -a PARTICLES_CHAR
declare -a PARTICLES_COLOR
declare -a PARTICLES_LIFE
declare -a PARTICLES_VX
declare -a PARTICLES_VY
PARTICLE_COUNT=0
MAX_PARTICLES=100

# Stars for night sky
declare -a STARS_X
declare -a STARS_Y
declare -a STARS_BRIGHTNESS
NUM_STARS=50

# Rain drops
declare -a RAIN_X
declare -a RAIN_Y
NUM_RAIN=30

# Flies
declare -a FLIES_X
declare -a FLIES_Y
declare -a FLIES_ALIVE
NUM_FLIES=10

# Screen buffer for double buffering
declare -a SCREEN_BUFFER

# Sound effects (terminal bell patterns)
sound_ribbit() {
    echo -ne "\a" 2>/dev/null || true
}

sound_chomp() {
    for i in {1..2}; do
        echo -ne "\a" 2>/dev/null || true
        sleep 0.05
    done
}

sound_explosion() {
    for i in {1..5}; do
        echo -ne "\a" 2>/dev/null || true
        sleep 0.02
    done
}

# Cursor control
cursor_to() {
    tput cup "$1" "$2"
}

hide_cursor() {
    tput civis 2>/dev/null || true
}

show_cursor() {
    tput cnorm 2>/dev/null || true
}

# Cleanup handler
cleanup() {
    show_cursor
    tput sgr0
    clear
    echo -e "${C_BRIGHT_GREEN}Thanks for watching ELI IS A FROG!${NC}"
    echo -e "Final Stats:"
    echo -e "  Flies Eaten: ${FLIES_EATEN}"
    echo -e "  Total Ribbits: ${TOTAL_RIBBITS}"
    echo -e "  Max Combo: ${MAX_COMBO}"
    echo -e "  Final Score: ${SCORE}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Initialize stars
init_stars() {
    for ((i=0; i<NUM_STARS; i++)); do
        STARS_X[$i]=$((RANDOM % TERM_WIDTH))
        STARS_Y[$i]=$((RANDOM % (TERM_HEIGHT - 10) + 1))
        STARS_BRIGHTNESS[$i]=$((RANDOM % 3))
    done
}

# Initialize rain
init_rain() {
    for ((i=0; i<NUM_RAIN; i++)); do
        RAIN_X[$i]=$((RANDOM % TERM_WIDTH))
        RAIN_Y[$i]=$((RANDOM % TERM_HEIGHT))
    done
}

# Initialize flies
init_flies() {
    for ((i=0; i<NUM_FLIES; i++)); do
        FLIES_X[$i]=$((RANDOM % (TERM_WIDTH - 10) + 5))
        FLIES_Y[$i]=$((RANDOM % 10 + 3))
        FLIES_ALIVE[$i]=1
    done
}

# Add particle
add_particle() {
    local x=$1 y=$2 char=$3 color=$4 life=$5 vx=$6 vy=$7
    if ((PARTICLE_COUNT < MAX_PARTICLES)); then
        PARTICLES_X[$PARTICLE_COUNT]=$x
        PARTICLES_Y[$PARTICLE_COUNT]=$y
        PARTICLES_CHAR[$PARTICLE_COUNT]=$char
        PARTICLES_COLOR[$PARTICLE_COUNT]=$color
        PARTICLES_LIFE[$PARTICLE_COUNT]=$life
        PARTICLES_VX[$PARTICLE_COUNT]=$vx
        PARTICLES_VY[$PARTICLE_COUNT]=$vy
        ((PARTICLE_COUNT++))
    fi
}

# Update particles
update_particles() {
    local new_count=0
    for ((i=0; i<PARTICLE_COUNT; i++)); do
        if ((PARTICLES_LIFE[$i] > 0)); then
            PARTICLES_X[$new_count]=$((PARTICLES_X[$i] + PARTICLES_VX[$i]))
            PARTICLES_Y[$new_count]=$((PARTICLES_Y[$i] + PARTICLES_VY[$i]))
            PARTICLES_CHAR[$new_count]=${PARTICLES_CHAR[$i]}
            PARTICLES_COLOR[$new_count]=${PARTICLES_COLOR[$i]}
            PARTICLES_LIFE[$new_count]=$((PARTICLES_LIFE[$i] - 1))
            PARTICLES_VX[$new_count]=${PARTICLES_VX[$i]}
            PARTICLES_VY[$new_count]=${PARTICLES_VY[$i]}
            ((new_count++))
        fi
    done
    PARTICLE_COUNT=$new_count
}

# Draw particles
draw_particles() {
    for ((i=0; i<PARTICLE_COUNT; i++)); do
        local x=${PARTICLES_X[$i]}
        local y=${PARTICLES_Y[$i]}
        if ((x >= 0 && x < TERM_WIDTH && y >= 0 && y < TERM_HEIGHT)); then
            cursor_to $y $x
            echo -ne "${PARTICLES_COLOR[$i]}${PARTICLES_CHAR[$i]}${NC}"
        fi
    done
}

# Create explosion effect
explosion() {
    local cx=$1 cy=$2
    local chars=("*" "+" "." "'" "°" "×" "•" "○")
    local colors=("${C_BRIGHT_RED}" "${C_BRIGHT_YELLOW}" "${C_YELLOW}" "${C_RED}")

    for ((i=0; i<30; i++)); do
        local angle=$((RANDOM % 360))
        local speed=$((RANDOM % 3 + 1))
        local vx=$(echo "scale=0; s($angle * 3.14159 / 180) * $speed" | bc -l 2>/dev/null || echo $((RANDOM % 3 - 1)))
        local vy=$(echo "scale=0; c($angle * 3.14159 / 180) * $speed" | bc -l 2>/dev/null || echo $((RANDOM % 3 - 1)))
        vx=${vx%.*}
        vy=${vy%.*}
        add_particle $cx $cy "${chars[$((RANDOM % ${#chars[@]}))]}" "${colors[$((RANDOM % ${#colors[@]}))]}" $((RANDOM % 10 + 5)) ${vx:-0} ${vy:-0}
    done
}

# Create sparkle effect
sparkle() {
    local cx=$1 cy=$2
    local chars=("✨" "⭐" "✦" "✧" "*" "+" "." "·")
    local colors=("${C_BRIGHT_YELLOW}" "${C_BRIGHT_WHITE}" "${C_BRIGHT_CYAN}" "${C_YELLOW}")

    for ((i=0; i<15; i++)); do
        local ox=$((RANDOM % 7 - 3))
        local oy=$((RANDOM % 5 - 2))
        add_particle $((cx + ox)) $((cy + oy)) "${chars[$((RANDOM % ${#chars[@]}))]}" "${colors[$((RANDOM % ${#colors[@]}))]}" $((RANDOM % 8 + 3)) 0 0
    done
}

# Matrix rain effect
matrix_column() {
    local x=$1
    local chars=("ア" "イ" "ウ" "エ" "オ" "カ" "キ" "ク" "ケ" "コ" "0" "1" "E" "L" "I" "F" "R" "O" "G")

    for ((y=0; y<TERM_HEIGHT; y++)); do
        cursor_to $y $x
        local brightness=$((255 - (y * 10)))
        ((brightness < 50)) && brightness=50
        echo -ne "$(rgb 0 $brightness 0)${chars[$((RANDOM % ${#chars[@]}))]}"
        sleep 0.01
    done
}

matrix_effect() {
    clear
    local pids=()
    for ((i=0; i<TERM_WIDTH; i+=2)); do
        matrix_column $i &
        pids+=($!)
        sleep 0.02
    done

    sleep 0.3
    for pid in "${pids[@]}"; do
        kill $pid 2>/dev/null || true
    done
    wait 2>/dev/null || true
}

# Draw weather effects
draw_weather() {
    case "${WEATHER}" in
        "rain")
            for ((i=0; i<NUM_RAIN; i++)); do
                cursor_to ${RAIN_Y[$i]} ${RAIN_X[$i]}
                echo -ne "${C_BRIGHT_BLUE}|${NC}"
                RAIN_Y[$i]=$(((RAIN_Y[$i] + 1) % TERM_HEIGHT))
                if ((RAIN_Y[$i] == 0)); then
                    RAIN_X[$i]=$((RANDOM % TERM_WIDTH))
                fi
            done
            ;;
        "storm")
            for ((i=0; i<NUM_RAIN; i++)); do
                cursor_to ${RAIN_Y[$i]} ${RAIN_X[$i]}
                echo -ne "${C_BRIGHT_CYAN}//${NC}"
                RAIN_Y[$i]=$(((RAIN_Y[$i] + 2) % TERM_HEIGHT))
                RAIN_X[$i]=$(((RAIN_X[$i] + 1) % TERM_WIDTH))
            done
            # Lightning flash
            if ((RANDOM % 50 == 0)); then
                echo -ne "\033[7m"
                sleep 0.05
                echo -ne "\033[0m"
            fi
            ;;
        "snow")
            local snow_chars=("❄" "❅" "❆" "*" "." "·")
            for ((i=0; i<NUM_RAIN; i++)); do
                cursor_to ${RAIN_Y[$i]} ${RAIN_X[$i]}
                echo -ne "${C_BRIGHT_WHITE}${snow_chars[$((RANDOM % ${#snow_chars[@]}))]}${NC}"
                RAIN_Y[$i]=$(((RAIN_Y[$i] + 1) % TERM_HEIGHT))
                RAIN_X[$i]=$(((RAIN_X[$i] + (RANDOM % 3) - 1 + TERM_WIDTH) % TERM_WIDTH))
            done
            ;;
    esac
}

# Draw stars (night mode)
draw_stars() {
    local star_chars=("." "·" "*" "✦" "★")
    for ((i=0; i<NUM_STARS; i++)); do
        cursor_to ${STARS_Y[$i]} ${STARS_X[$i]}
        local brightness=${STARS_BRIGHTNESS[$i]}
        # Twinkle effect
        if ((RANDOM % 20 == 0)); then
            STARS_BRIGHTNESS[$i]=$(((brightness + 1) % 3))
        fi
        case $brightness in
            0) echo -ne "${C_DIM}.${NC}" ;;
            1) echo -ne "${C_WHITE}·${NC}" ;;
            2) echo -ne "${C_BRIGHT_WHITE}*${NC}" ;;
        esac
    done
}

# Draw moon with phases
draw_moon() {
    local phase=$((LEVEL % 8))
    local moon_x=$((TERM_WIDTH - 15))
    local moon_y=3

    cursor_to $moon_y $moon_x
    case $phase in
        0) # New moon
            echo -ne "${C_DIM}   ███   ${NC}"
            cursor_to $((moon_y + 1)) $moon_x
            echo -ne "${C_DIM}  █████  ${NC}"
            cursor_to $((moon_y + 2)) $moon_x
            echo -ne "${C_DIM}   ███   ${NC}"
            ;;
        1|7) # Crescent
            echo -ne "${C_BRIGHT_YELLOW}   ██    ${NC}"
            cursor_to $((moon_y + 1)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}  ███    ${NC}"
            cursor_to $((moon_y + 2)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}   ██    ${NC}"
            ;;
        2|6) # Half
            echo -ne "${C_BRIGHT_YELLOW}   ███   ${NC}"
            cursor_to $((moon_y + 1)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}  ████   ${NC}"
            cursor_to $((moon_y + 2)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}   ███   ${NC}"
            ;;
        3|5) # Gibbous
            echo -ne "${C_BRIGHT_YELLOW}   ████  ${NC}"
            cursor_to $((moon_y + 1)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}  █████  ${NC}"
            cursor_to $((moon_y + 2)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}   ████  ${NC}"
            ;;
        4) # Full moon
            echo -ne "${C_BRIGHT_YELLOW}   ███   ${NC}"
            cursor_to $((moon_y + 1)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}  █████  ${NC}"
            cursor_to $((moon_y + 2)) $moon_x
            echo -ne "${C_BRIGHT_YELLOW}   ███   ${NC}"
            ;;
    esac
}

# Draw sun with rays
draw_sun() {
    local sun_x=$((TERM_WIDTH - 20))
    local sun_y=3
    local frame=$((SCORE % 4))

    local rays1="\\  |  /"
    local rays2=" \\ | / "
    local rays3="--   --"
    local rays4=" / | \\ "
    local rays5="/  |  \\"

    cursor_to $sun_y $sun_x
    case $frame in
        0|2)
            echo -ne "${C_BRIGHT_YELLOW}  \\ | /  ${NC}"
            cursor_to $((sun_y + 1)) $sun_x
            echo -ne "${C_BRIGHT_YELLOW} --${C_YELLOW}███${C_BRIGHT_YELLOW}-- ${NC}"
            cursor_to $((moon_y + 2)) $sun_x
            echo -ne "${C_BRIGHT_YELLOW}  / | \\  ${NC}"
            ;;
        1|3)
            echo -ne "${C_YELLOW}   \\|/   ${NC}"
            cursor_to $((sun_y + 1)) $sun_x
            echo -ne "${C_YELLOW}  -${C_BRIGHT_YELLOW}███${C_YELLOW}-  ${NC}"
            cursor_to $((sun_y + 2)) $sun_x
            echo -ne "${C_YELLOW}   /|\\   ${NC}"
            ;;
    esac
}

# Complex frog with emotions and animations
draw_eli() {
    local x=${ELI_X}
    local y=${ELI_Y}
    local emotion=$1
    local frame=$2

    # Frog shadow
    cursor_to $((y + 4)) $((x - 1))
    echo -ne "${C_DIM}  ▄▄▄▄▄▄  ${NC}"

    case $emotion in
        "happy")
            cursor_to $y $x
            echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}^^${NC}$(color256 46)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 46)  (${C_BRIGHT_YELLOW}^▽^${NC}$(color256 46))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 40) (${NC}$(color256 46) >__< ${NC}$(color256 40)) ${NC}"
            cursor_to $((y + 3)) $x
            if ((frame % 2 == 0)); then
                echo -ne "$(color256 40)  ^^  ^^  ${NC}"
            else
                echo -ne "$(color256 40)  ^    ^  ${NC}"
            fi
            ;;
        "eating")
            cursor_to $y $x
            echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}◉◉${NC}$(color256 46)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 46)  (${C_BRIGHT_RED}○${NC}$(color256 46))────${C_YELLOW}*${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 40) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 40)  ^    ^  ${NC}"
            ;;
        "jumping")
            local jump_offset=$((frame % 4))
            cursor_to $((y - jump_offset)) $x
            echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}°°${NC}$(color256 46)@   ${NC}"
            cursor_to $((y - jump_offset + 1)) $x
            echo -ne "$(color256 46)  (${C_BRIGHT_GREEN}○○${NC}$(color256 46))  ${NC}"
            cursor_to $((y - jump_offset + 2)) $x
            echo -ne "$(color256 40) \\(>__<)/ ${NC}"
            cursor_to $((y - jump_offset + 3)) $x
            echo -ne "$(color256 40)   V  V   ${NC}"
            ;;
        "sleeping")
            cursor_to $y $x
            echo -ne "$(color256 34)   @${C_DIM}--${NC}$(color256 34)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 34)  (${C_DIM}u.u${NC}$(color256 34))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 28) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 28)  ^    ^  ${NC}"
            # Zzz
            cursor_to $((y - 1)) $((x + 10))
            echo -ne "${C_BRIGHT_CYAN}z${NC}"
            cursor_to $((y - 2)) $((x + 12))
            echo -ne "${C_CYAN}Z${NC}"
            cursor_to $((y - 3)) $((x + 14))
            echo -ne "${C_BRIGHT_CYAN}z${NC}"
            ;;
        "angry")
            cursor_to $y $x
            echo -ne "$(color256 196)   @${C_BRIGHT_RED}><${NC}$(color256 196)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 196)  (${C_BRIGHT_RED}╬ಠ益ಠ${NC}$(color256 196))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 160) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 160)  ^^  ^^  ${NC}"
            # Anger symbol
            cursor_to $((y - 1)) $((x + 8))
            echo -ne "${C_BRIGHT_RED}💢${NC}"
            ;;
        "singing")
            cursor_to $y $x
            echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}◕◕${NC}$(color256 46)@ ♪ ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 46)  (${C_BRIGHT_MAGENTA}°▽°${NC}$(color256 46))♫  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 40) ( >__< )  ${NC}"
            cursor_to $((y + 3)) $x
            if ((frame % 2 == 0)); then
                echo -ne "$(color256 40)  ^    ^   ${NC}"
            else
                echo -ne "$(color256 40)   ^  ^    ${NC}"
            fi
            ;;
        "scared")
            cursor_to $y $x
            echo -ne "$(color256 255)   @${C_BRIGHT_WHITE}OO${NC}$(color256 255)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 255)  (${C_BRIGHT_YELLOW}°Д°${NC}$(color256 255))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 250) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 250)  ^    ^  ${NC}"
            ;;
        "cool")
            cursor_to $y $x
            echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}▀▀${NC}$(color256 46)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 46)  (${C_BLACK}■${C_BRIGHT_GREEN}_${C_BLACK}■${NC}$(color256 46))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 40) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 40)  ^    ^  ${NC}"
            ;;
        "love")
            cursor_to $y $x
            echo -ne "$(color256 213)   @${C_BRIGHT_RED}♥♥${NC}$(color256 213)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 213)  (${C_BRIGHT_MAGENTA}´∀\`${NC}$(color256 213))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 207) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 207)  ^    ^  ${NC}"
            # Hearts floating
            for ((h=0; h<3; h++)); do
                cursor_to $((y - h - 1)) $((x + 10 + (RANDOM % 5)))
                echo -ne "${C_BRIGHT_RED}♥${NC}"
            done
            ;;
        "dead")
            cursor_to $y $x
            echo -ne "$(color256 242)   @${C_DIM}xx${NC}$(color256 242)@   ${NC}"
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 242)  (${C_DIM}x_x${NC}$(color256 242))  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 238)  (>__<)  ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 238)   ~~~~   ${NC}"
            ;;
        *)  # normal/idle
            cursor_to $y $x
            if ((frame % 20 < 2)); then
                # Blink
                echo -ne "$(color256 46)   @${C_DIM}--${NC}$(color256 46)@   ${NC}"
            else
                echo -ne "$(color256 46)   @${C_BRIGHT_WHITE}..${NC}$(color256 46)@   ${NC}"
            fi
            cursor_to $((y + 1)) $x
            echo -ne "$(color256 46)  (----)  ${NC}"
            cursor_to $((y + 2)) $x
            echo -ne "$(color256 40) ( >__< ) ${NC}"
            cursor_to $((y + 3)) $x
            echo -ne "$(color256 40)  ^    ^  ${NC}"
            ;;
    esac
}

# Draw flies with animation
draw_flies() {
    local frame=$1
    for ((i=0; i<NUM_FLIES; i++)); do
        if ((FLIES_ALIVE[$i] == 1)); then
            local x=${FLIES_X[$i]}
            local y=${FLIES_Y[$i]}

            # Move fly randomly
            FLIES_X[$i]=$(((x + RANDOM % 5 - 2 + TERM_WIDTH) % (TERM_WIDTH - 5) + 2))
            FLIES_Y[$i]=$(((y + RANDOM % 3 - 1 + TERM_HEIGHT - 15) % (TERM_HEIGHT - 18) + 3))

            cursor_to $y $x
            if ((frame % 2 == 0)); then
                echo -ne "${C_BRIGHT_WHITE}°${C_DIM}~${NC}"
            else
                echo -ne "${C_DIM}~${C_BRIGHT_WHITE}°${NC}"
            fi
        fi
    done
}

# Draw lilypad with ripples
draw_lilypad() {
    local x=$1
    local y=$2
    local frame=$3

    # Ripples
    local ripple_chars=("·" "." "," " ")
    local ripple=${ripple_chars[$((frame % 4))]}

    cursor_to $((y)) $((x - 5))
    echo -ne "${C_CYAN}${ripple}${NC}"
    cursor_to $((y)) $((x + 15))
    echo -ne "${C_CYAN}${ripple}${NC}"

    cursor_to $((y + 1)) $((x - 2))
    echo -ne "$(color256 22)  ▄▄▄▄▄▄▄▄▄▄▄▄  ${NC}"
    cursor_to $((y + 2)) $((x - 2))
    echo -ne "$(color256 28) ▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ${NC}"
}

# Draw pond with waves
draw_pond() {
    local frame=$1
    local wave_chars=("~" "≈" "∼" "˜")
    local wave=${wave_chars[$((frame % 4))]}

    for ((y=TERM_HEIGHT-8; y<TERM_HEIGHT-2; y++)); do
        cursor_to $y 0
        for ((x=0; x<TERM_WIDTH; x++)); do
            if (((x + y + frame) % 4 == 0)); then
                echo -ne "$(color256 27)${wave}${NC}"
            elif (((x + y + frame) % 4 == 1)); then
                echo -ne "$(color256 33)${wave}${NC}"
            elif (((x + y + frame) % 4 == 2)); then
                echo -ne "$(color256 39)≈${NC}"
            else
                echo -ne "$(color256 45)~${NC}"
            fi
        done
    done
}

# Draw cattails/reeds
draw_reeds() {
    local positions=(5 12 70 80 95)
    local frame=$1

    for pos in "${positions[@]}"; do
        if ((pos < TERM_WIDTH)); then
            for ((h=0; h<6; h++)); do
                cursor_to $((TERM_HEIGHT - 10 - h)) $pos
                if ((h == 5)); then
                    echo -ne "$(color256 94)▄${NC}"
                elif ((h == 4)); then
                    echo -ne "$(color256 94)█${NC}"
                else
                    if (((frame + h) % 3 == 0)); then
                        echo -ne "$(color256 22) │${NC}"
                    else
                        echo -ne "$(color256 22)│ ${NC}"
                    fi
                fi
            done
        fi
    done
}

# Draw dragonflies
draw_dragonflies() {
    local frame=$1
    local df_x=$(((frame * 3) % TERM_WIDTH))
    local df_y=$((8 + (frame % 5)))

    cursor_to $df_y $df_x
    if ((frame % 2 == 0)); then
        echo -ne "${C_BRIGHT_CYAN}═══●${C_BRIGHT_BLUE}◗${NC}"
    else
        echo -ne "${C_BRIGHT_BLUE}◖${C_BRIGHT_CYAN}●═══${NC}"
    fi
}

# Boss: The Great Heron
draw_boss() {
    local x=$1
    local y=$2
    local health=${BOSS_HEALTH}
    local frame=$3

    # Health bar
    cursor_to 2 $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_RED}BOSS: THE GREAT HERON${NC}"
    cursor_to 3 $((TERM_WIDTH/2 - 20))
    echo -ne "["
    local health_bars=$((health / 5))
    for ((i=0; i<20; i++)); do
        if ((i < health_bars)); then
            echo -ne "${C_BRIGHT_RED}█${NC}"
        else
            echo -ne "${C_DIM}░${NC}"
        fi
    done
    echo -ne "] ${health}%"

    # Boss body
    cursor_to $y $x
    if ((frame % 4 < 2)); then
        echo -ne "${C_WHITE}      ▄▄▄${NC}"
        cursor_to $((y+1)) $x
        echo -ne "${C_WHITE}     █${C_YELLOW}▀${C_WHITE}██${NC}"
        cursor_to $((y+2)) $x
        echo -ne "${C_WHITE}    ████████${NC}"
        cursor_to $((y+3)) $x
        echo -ne "${C_WHITE}   ██${C_DIM}║${C_WHITE}██${C_DIM}║${C_WHITE}██${NC}"
        cursor_to $((y+4)) $x
        echo -ne "${C_WHITE}  ███${C_DIM}║${C_WHITE}██${C_DIM}║${C_WHITE}███${NC}"
        cursor_to $((y+5)) $x
        echo -ne "${C_YELLOW}     ║  ║${NC}"
        cursor_to $((y+6)) $x
        echo -ne "${C_YELLOW}    ═╝  ╚═${NC}"
    else
        echo -ne "${C_WHITE}      ▄▄▄${NC}"
        cursor_to $((y+1)) $x
        echo -ne "${C_WHITE}     █${C_RED}◆${C_WHITE}██${NC}"
        cursor_to $((y+2)) $x
        echo -ne "${C_WHITE}    ████████${NC}"
        cursor_to $((y+3)) $x
        echo -ne "${C_WHITE}   ███████████${NC}"
        cursor_to $((y+4)) $x
        echo -ne "${C_WHITE}  ██████${C_DIM}▼${C_WHITE}████${NC}"
        cursor_to $((y+5)) $x
        echo -ne "${C_YELLOW}     ║  ║${NC}"
        cursor_to $((y+6)) $x
        echo -ne "${C_YELLOW}    ═╝  ╚═${NC}"
    fi
}

# Draw UI/HUD
draw_hud() {
    # Top bar
    cursor_to 0 0
    echo -ne "$(bg256 236)$(color256 46) 🐸 ELI IS A FROG "
    echo -ne "$(color256 255)| Score: ${SCORE} "
    echo -ne "| Flies: ${FLIES_EATEN} "
    echo -ne "| Combo: ${COMBO}x "
    echo -ne "| Level: ${LEVEL} "

    # Health bar
    echo -ne "| HP: ["
    local hp=${HEALTH}
    local hp_bars=$((hp / 10))
    for ((i=0; i<10; i++)); do
        if ((i < hp_bars)); then
            echo -ne "$(color256 46)█${NC}"
        else
            echo -ne "$(color256 236)░${NC}"
        fi
    done
    echo -ne "$(bg256 236)] "

    # Padding to fill line
    local padding=$((TERM_WIDTH - 80))
    ((padding > 0)) && printf "%${padding}s" " "
    echo -ne "${NC}"
}

# Title screen with animation
title_screen() {
    clear

    local frame=0

    # Show animated title for 60 frames (~3 seconds) then auto-start
    while ((frame < 25)); do
        clear

        # Animated background
        for ((y=0; y<TERM_HEIGHT; y++)); do
            cursor_to $y 0
            for ((x=0; x<TERM_WIDTH; x++)); do
                if (((x + y + frame) % 20 == 0)); then
                    echo -ne "$(color256 $((22 + (frame % 6))))·${NC}"
                else
                    echo -ne " "
                fi
            done
        done

        # Title with color cycling
        local title_color=$((46 + (frame % 10)))
        cursor_to 5 $((TERM_WIDTH/2 - 35))
        echo -ne "$(color256 $title_color)"
        cat << 'EOF'
███████╗██╗     ██╗    ██╗███████╗     █████╗     ███████╗██████╗  ██████╗  ██████╗
██╔════╝██║     ██║    ██║██╔════╝    ██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗██╔════╝
█████╗  ██║     ██║    ██║███████╗    ███████║    █████╗  ██████╔╝██║   ██║██║  ███╗
██╔══╝  ██║     ██║    ██║╚════██║    ██╔══██║    ██╔══╝  ██╔══██╗██║   ██║██║   ██║
███████╗███████╗██║    ██║███████║    ██║  ██║    ██║     ██║  ██║╚██████╔╝╚██████╔╝
╚══════╝╚══════╝╚═╝    ╚═╝╚══════╝    ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝
EOF
        echo -ne "${NC}"

        # Subtitle
        cursor_to 13 $((TERM_WIDTH/2 - 25))
        echo -ne "${C_BRIGHT_YELLOW}✦ THE ULTIMATE CINEMATIC EXPERIENCE ✦${NC}"
        cursor_to 14 $((TERM_WIDTH/2 - 20))
        echo -ne "${C_CYAN}Director's Cut Extended Edition${NC}"

        # Dancing frogs
        local frog_y=17
        for ((f=0; f<5; f++)); do
            local frog_x=$((TERM_WIDTH/2 - 30 + f*15))
            cursor_to $frog_y $frog_x
            if (((frame + f) % 4 < 2)); then
                echo -ne "$(color256 46) @..@ ${NC}"
                cursor_to $((frog_y+1)) $frog_x
                echo -ne "$(color256 46)(^▽^)${NC}"
            else
                echo -ne "$(color256 46) @^^@ ${NC}"
                cursor_to $((frog_y+1)) $frog_x
                echo -ne "$(color256 46)(°▽°)${NC}"
            fi
        done

        # Starting soon message
        local countdown=$(( (60 - frame) / 20 + 1 ))
        cursor_to $((TERM_HEIGHT - 5)) $((TERM_WIDTH/2 - 15))
        echo -ne "${C_BRIGHT_WHITE}>>> STARTING IN ${countdown}... <<<${NC}"

        # Credits teaser
        cursor_to $((TERM_HEIGHT - 3)) $((TERM_WIDTH/2 - 20))
        echo -ne "${C_DIM}A Claude Code Productions Film${NC}"

        ((frame++))
        sleep 0.05
    done
}

# Scene transitions
transition_fade() {
    local direction=$1  # "in" or "out"
    local chars=("░" "▒" "▓" "█")

    if [[ "$direction" == "out" ]]; then
        for level in {0..3}; do
            for ((y=0; y<TERM_HEIGHT; y++)); do
                cursor_to $y 0
                for ((x=0; x<TERM_WIDTH; x++)); do
                    echo -ne "${C_DIM}${chars[$level]}${NC}"
                done
            done
            sleep 0.03
        done
    else
        for level in {3..0}; do
            for ((y=0; y<TERM_HEIGHT; y++)); do
                cursor_to $y 0
                for ((x=0; x<TERM_WIDTH; x++)); do
                    echo -ne "${C_DIM}${chars[$level]}${NC}"
                done
            done
            sleep 0.03
        done
    fi
    clear
}

transition_wipe() {
    for ((x=0; x<TERM_WIDTH; x+=2)); do
        for ((y=0; y<TERM_HEIGHT; y++)); do
            cursor_to $y $x
            echo -ne "$(color256 $((22 + (x % 10))))██${NC}"
        done
        sleep 0.01
    done
    clear
}

transition_circle() {
    local cx=$((TERM_WIDTH / 2))
    local cy=$((TERM_HEIGHT / 2))
    local max_r=$((TERM_WIDTH > TERM_HEIGHT ? TERM_WIDTH : TERM_HEIGHT))

    for ((r=0; r<max_r; r+=2)); do
        for ((angle=0; angle<360; angle+=10)); do
            local x=$(echo "scale=0; $cx + $r * c($angle * 3.14159 / 180)" | bc -l 2>/dev/null || echo $cx)
            local y=$(echo "scale=0; $cy + ($r/2) * s($angle * 3.14159 / 180)" | bc -l 2>/dev/null || echo $cy)
            x=${x%.*}
            y=${y%.*}
            if ((x >= 0 && x < TERM_WIDTH && y >= 0 && y < TERM_HEIGHT)); then
                cursor_to ${y:-$cy} ${x:-$cx}
                echo -ne "$(color256 46)█${NC}"
            fi
        done
        sleep 0.02
    done
    clear
}

# Scrolling text
scroll_text() {
    local text="$1"
    local y=$2
    local delay=${3:-0.05}

    cursor_to $y 0
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
}

# Typewriter effect
typewriter() {
    local text="$1"
    local y=$2
    local x=$3
    local delay=${4:-0.03}

    cursor_to $y $x
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
}

# Dramatic pause with dots
dramatic_pause() {
    local y=$1
    local x=$2
    local msg="$3"

    cursor_to $y $x
    echo -n "$msg"
    for i in {1..3}; do
        sleep 0.2
        echo -n "."
    done
    sleep 0.2
}

# Scene: The Normal Life
scene_normal_life() {
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_CYAN}═══ CHAPTER 1 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}THE NORMAL LIFE${NC}"
    sleep 0.2

    transition_wipe

    local frame=0
    while ((frame < 15)); do
        clear

        # Office background
        cursor_to 2 5
        echo -ne "${C_DIM}╔════════════════════════════════════╗${NC}"
        cursor_to 3 5
        echo -ne "${C_DIM}║   ACME CORPORATION - CUBICLE 42   ║${NC}"
        cursor_to 4 5
        echo -ne "${C_DIM}╚════════════════════════════════════╝${NC}"

        # Desk
        cursor_to 15 20
        echo -ne "${C_YELLOW}┌──────────────────────┐${NC}"
        cursor_to 16 20
        echo -ne "${C_YELLOW}│ ${C_WHITE}[____] ${C_CYAN}☕ ${C_DIM}📄 📊${C_YELLOW}     │${NC}"
        cursor_to 17 20
        echo -ne "${C_YELLOW}└──────────────────────┘${NC}"

        # Human Eli (stick figure in office)
        local eli_x=30
        local eli_y=11
        cursor_to $eli_y $eli_x
        echo -ne "${C_BRIGHT_YELLOW}  O  ${NC}"
        cursor_to $((eli_y+1)) $eli_x
        echo -ne "${C_BRIGHT_YELLOW} /|\\ ${NC}"
        cursor_to $((eli_y+2)) $eli_x
        echo -ne "${C_BRIGHT_YELLOW} / \\ ${NC}"

        # Thought bubble
        if ((frame > 20)); then
            cursor_to 6 45
            echo -ne "${C_WHITE}  .-~~~-.${NC}"
            cursor_to 7 45
            echo -ne "${C_WHITE} /  ◠ ◠  \\${NC}"
            cursor_to 8 45
            echo -ne "${C_WHITE}|  there  |${NC}"
            cursor_to 9 45
            echo -ne "${C_WHITE}|  must   |${NC}"
            cursor_to 10 45
            echo -ne "${C_WHITE}|   be    |${NC}"
            cursor_to 11 45
            echo -ne "${C_WHITE}|  more   |${NC}"
            cursor_to 12 45
            echo -ne "${C_WHITE}|  to...  |${NC}"
            cursor_to 13 45
            echo -ne "${C_WHITE} \\      /${NC}"
            cursor_to 14 45
            echo -ne "${C_WHITE}  '-..-'${NC}"
            cursor_to 15 42
            echo -ne "${C_WHITE}○${NC}"
            cursor_to 15 40
            echo -ne "${C_WHITE}○${NC}"
        fi

        # Clock ticking
        cursor_to 2 60
        local hour=$((9 + frame / 20))
        echo -ne "${C_DIM}🕐 ${hour}:00${NC}"

        ((frame++))
        sleep 0.02
    done

    # Eli sighs
    cursor_to 20 30
    typewriter "Eli: *sigh* Another day, another spreadsheet..." 20 15
    sleep 0.3
}

# Scene: The Discovery
scene_discovery() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_CYAN}═══ CHAPTER 2 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}THE DISCOVERY${NC}"
    sleep 0.2

    transition_wipe

    local frame=0

    # Walking in the park
    while ((frame < 25)); do
        clear

        # Park background
        for ((y=TERM_HEIGHT-6; y<TERM_HEIGHT; y++)); do
            cursor_to $y 0
            for ((x=0; x<TERM_WIDTH; x++)); do
                if ((y == TERM_HEIGHT-6)); then
                    echo -ne "$(color256 34)▓${NC}"
                else
                    echo -ne "$(color256 28)░${NC}"
                fi
            done
        done

        # Trees
        local trees=(10 30 55 75 90)
        for tx in "${trees[@]}"; do
            if ((tx < TERM_WIDTH)); then
                cursor_to $((TERM_HEIGHT-10)) $tx
                echo -ne "$(color256 22)  🌳  ${NC}"
            fi
        done

        # Eli walking
        local eli_walk_x=$((frame * 2))
        cursor_to $((TERM_HEIGHT-9)) $eli_walk_x
        if ((frame % 2 == 0)); then
            echo -ne "${C_BRIGHT_YELLOW}  O  ${NC}"
            cursor_to $((TERM_HEIGHT-8)) $eli_walk_x
            echo -ne "${C_BRIGHT_YELLOW} /|\\ ${NC}"
            cursor_to $((TERM_HEIGHT-7)) $eli_walk_x
            echo -ne "${C_BRIGHT_YELLOW} / \\ ${NC}"
        else
            echo -ne "${C_BRIGHT_YELLOW}  O  ${NC}"
            cursor_to $((TERM_HEIGHT-8)) $eli_walk_x
            echo -ne "${C_BRIGHT_YELLOW} /|\\ ${NC}"
            cursor_to $((TERM_HEIGHT-7)) $eli_walk_x
            echo -ne "${C_BRIGHT_YELLOW}  X  ${NC}"
        fi

        # Mysterious glow in the distance
        if ((frame > 30)); then
            cursor_to $((TERM_HEIGHT-10)) $((TERM_WIDTH-20))
            echo -ne "$(color256 $((82 + (frame % 5))))✨ ✨ ✨${NC}"
            cursor_to $((TERM_HEIGHT-9)) $((TERM_WIDTH-20))
            echo -ne "$(color256 $((118 + (frame % 5))))  ???  ${NC}"
        fi

        ((frame++))
        sleep 0.02
    done

    # Found the magical pond
    clear
    cursor_to 10 $((TERM_WIDTH/2 - 20))
    typewriter "Eli discovered a mystical glowing pond..." 10 $((TERM_WIDTH/2 - 25))
    sleep 0.3

    # Pond reveal
    for glow in {1..20}; do
        clear

        # Glowing pond
        cursor_to 12 $((TERM_WIDTH/2 - 15))
        echo -ne "$(color256 $((44 + glow % 6)))    ~~~~≈≈≈~~~~    ${NC}"
        cursor_to 13 $((TERM_WIDTH/2 - 15))
        echo -ne "$(color256 $((50 + glow % 6)))  ≈≈≈≈≈✨≈≈≈≈≈≈  ${NC}"
        cursor_to 14 $((TERM_WIDTH/2 - 15))
        echo -ne "$(color256 $((44 + glow % 6)))    ~~~~≈≈≈~~~~    ${NC}"

        sparkle $((TERM_WIDTH/2)) 13
        draw_particles
        update_particles

        sleep 0.03
    done

    cursor_to 18 $((TERM_WIDTH/2 - 20))
    typewriter "Voice: 'Drink from the pond, Eli...'" 18 $((TERM_WIDTH/2 - 20))
    sleep 0.3
    cursor_to 20 $((TERM_WIDTH/2 - 20))
    typewriter "Voice: 'Embrace your true nature...'" 20 $((TERM_WIDTH/2 - 20))
    sleep 0.2
}

# Scene: The Transformation
scene_transformation() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_MAGENTA}═══ CHAPTER 3 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}THE TRANSFORMATION${NC}"
    sleep 0.2

    # Matrix-like effect
    clear
    echo -ne "${C_BRIGHT_GREEN}"
    for ((y=0; y<TERM_HEIGHT; y++)); do
        cursor_to $y 0
        for ((x=0; x<TERM_WIDTH; x++)); do
            if ((RANDOM % 10 == 0)); then
                echo -ne "█"
            elif ((RANDOM % 8 == 0)); then
                echo -ne "▓"
            elif ((RANDOM % 5 == 0)); then
                echo -ne "░"
            else
                echo -ne " "
            fi
        done
        sleep 0.02
    done
    echo -ne "${NC}"
    sleep 0.2

    # Transformation sequence
    local stages=(
        "Human Eli stands at the pond's edge..."
        "The water begins to glow brighter..."
        "Eli drinks from the mystical waters..."
        "A tingling sensation spreads through his body..."
        "His skin turns green..."
        "His eyes grow larger..."
        "His legs become powerful..."
        "RIBBIT! The transformation is complete!"
    )

    for stage in "${stages[@]}"; do
        clear

        # Background magic
        for ((y=0; y<TERM_HEIGHT; y++)); do
            cursor_to $y 0
            for ((x=0; x<TERM_WIDTH; x++)); do
                if ((RANDOM % 30 == 0)); then
                    echo -ne "$(color256 $((46 + RANDOM % 50)))✨${NC}"
                else
                    echo -ne " "
                fi
            done
        done

        cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - ${#stage}/2))
        echo -ne "${C_BRIGHT_YELLOW}${stage}${NC}"

        # Sound effect
        sound_ribbit

        sleep 0.3
    done

    # Final transformation reveal
    clear
    ELI_X=$((TERM_WIDTH/2 - 5))
    ELI_Y=$((TERM_HEIGHT/2 - 2))

    for ((glow=0; glow<30; glow++)); do
        clear

        # Radial glow
        for ((r=15; r>0; r--)); do
            local color=$((46 + 15 - r))
            for ((angle=0; angle<360; angle+=30)); do
                local x=$(echo "scale=0; ${ELI_X} + 5 + $r * c($angle * 3.14159 / 180)" | bc -l 2>/dev/null || echo ${ELI_X})
                local y=$(echo "scale=0; ${ELI_Y} + 2 + ($r/3) * s($angle * 3.14159 / 180)" | bc -l 2>/dev/null || echo ${ELI_Y})
                x=${x%.*}
                y=${y%.*}
                if ((x >= 0 && x < TERM_WIDTH && y >= 0 && y < TERM_HEIGHT)); then
                    cursor_to ${y:-10} ${x:-40}
                    echo -ne "$(color256 $color)*${NC}"
                fi
            done
        done

        draw_eli "happy" $glow

        sleep 0.03
    done

    cursor_to $((TERM_HEIGHT - 3)) $((TERM_WIDTH/2 - 10))
    echo -ne "${C_BRIGHT_GREEN}🐸 ELI IS NOW A FROG! 🐸${NC}"
    sleep 0.2
}

# Scene: Learning to be a frog
scene_frog_training() {
    transition_circle
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_CYAN}═══ CHAPTER 4 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}FROG TRAINING MONTAGE${NC}"
    sleep 0.2

    init_flies

    # Training montage music (visual representation)
    local training_phases=(
        "LESSON 1: THE HOP"
        "LESSON 2: THE TONGUE"
        "LESSON 3: THE RIBBIT"
        "LESSON 4: THE SWIM"
        "LESSON 5: CATCHING FLIES"
    )

    for phase in "${training_phases[@]}"; do
        clear
        cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
        echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

        case "$phase" in
            *"HOP"*)
                for ((hop=0; hop<20; hop++)); do
                    clear
                    cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
                    echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

                    ELI_X=$((20 + hop * 4))
                    draw_eli "jumping" $hop

                    # Jump arc
                    local arc_y=$((15 - (hop % 5) * 2 + (hop % 5 > 2 ? (hop % 5 - 2) * 2 : 0)))
                    ELI_Y=$arc_y

                    sleep 0.03
                done
                ;;
            *"TONGUE"*)
                ELI_X=$((TERM_WIDTH/2 - 5))
                ELI_Y=12
                for ((t=0; t<15; t++)); do
                    clear
                    cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
                    echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

                    if ((t % 5 < 3)); then
                        draw_eli "eating" $t
                    else
                        draw_eli "happy" $t
                    fi

                    sleep 0.05
                done
                ;;
            *"RIBBIT"*)
                ELI_X=$((TERM_WIDTH/2 - 5))
                ELI_Y=12
                for ((r=0; r<15; r++)); do
                    clear
                    cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
                    echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

                    draw_eli "singing" $r

                    # Ribbit text expanding
                    local ribbit_size=$((r % 5))
                    case $ribbit_size in
                        0) cursor_to 10 $((TERM_WIDTH/2 + 10)); echo -ne "${C_BRIGHT_GREEN}ribbit${NC}" ;;
                        1) cursor_to 9 $((TERM_WIDTH/2 + 10)); echo -ne "${C_BRIGHT_GREEN}RIBBIT${NC}" ;;
                        2) cursor_to 8 $((TERM_WIDTH/2 + 10)); echo -ne "${C_BRIGHT_YELLOW}RIBBIT!${NC}" ;;
                        3) cursor_to 7 $((TERM_WIDTH/2 + 10)); echo -ne "${C_BRIGHT_YELLOW}RIBBIT!!${NC}" ;;
                        4) cursor_to 6 $((TERM_WIDTH/2 + 8)); echo -ne "${C_BRIGHT_RED}RIBBIIIIT!!!${NC}" ;;
                    esac

                    ((TOTAL_RIBBITS++))
                    sleep 0.05
                done
                ;;
            *"SWIM"*)
                for ((s=0; s<30; s++)); do
                    clear
                    cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
                    echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

                    # Water
                    draw_pond $s

                    ELI_X=$((10 + s * 3))
                    ELI_Y=10
                    draw_eli "happy" $s

                    sleep 0.02
                done
                ;;
            *"FLIES"*)
                ELI_X=$((TERM_WIDTH/2 - 5))
                ELI_Y=12
                init_flies
                for ((f=0; f<40; f++)); do
                    clear
                    cursor_to 2 $((TERM_WIDTH/2 - ${#phase}/2))
                    echo -ne "${C_BRIGHT_YELLOW}🎵 ${phase} 🎵${NC}"

                    draw_flies $f

                    # Check if Eli catches a fly
                    for ((i=0; i<NUM_FLIES; i++)); do
                        if ((FLIES_ALIVE[$i] == 1)); then
                            local dx=$((FLIES_X[$i] - ELI_X))
                            local dy=$((FLIES_Y[$i] - ELI_Y))
                            if ((dx > -5 && dx < 15 && dy > -2 && dy < 6 && RANDOM % 10 == 0)); then
                                FLIES_ALIVE[$i]=0
                                ((FLIES_EATEN++))
                                ((SCORE += 100))
                                explosion ${FLIES_X[$i]} ${FLIES_Y[$i]}
                                sound_chomp
                            fi
                        fi
                    done

                    if ((f % 8 < 4)); then
                        draw_eli "eating" $f
                    else
                        draw_eli "happy" $f
                    fi

                    draw_particles
                    update_particles

                    # Score display
                    cursor_to 4 5
                    echo -ne "${C_BRIGHT_WHITE}Flies caught: ${FLIES_EATEN}${NC}"

                    sleep 0.03
                done
                ;;
        esac

        sleep 0.2
    done

    # Training complete
    clear
    cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_GREEN}✓ TRAINING COMPLETE! ✓${NC}"
    cursor_to $((TERM_HEIGHT/2 + 2)) $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_YELLOW}Eli has mastered the way of the frog!${NC}"
    sleep 0.2
}

# Scene: A day in the life
scene_day_in_life() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_CYAN}═══ CHAPTER 5 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_WHITE}A DAY IN THE LIFE OF A FROG${NC}"
    sleep 0.2

    init_stars
    init_rain
    init_flies

    local time_of_day=("DAWN" "MORNING" "NOON" "AFTERNOON" "DUSK" "NIGHT")
    local weathers=("clear" "clear" "rain" "clear" "clear" "clear")

    for ((tod=0; tod<6; tod++)); do
        WEATHER=${weathers[$tod]}

        for ((frame=0; frame<40; frame++)); do
            clear

            # Time indicator
            cursor_to 1 $((TERM_WIDTH/2 - 5))
            echo -ne "${C_BRIGHT_CYAN}☀ ${time_of_day[$tod]} ☀${NC}"

            # Sky color based on time
            case $tod in
                0) # Dawn
                    for ((y=2; y<8; y++)); do
                        cursor_to $y 0
                        echo -ne "$(bg256 $((52 + y)))$(printf '%*s' $TERM_WIDTH '')${NC}"
                    done
                    ;;
                1|2|3) # Day
                    for ((y=2; y<8; y++)); do
                        cursor_to $y 0
                        echo -ne "$(bg256 $((39 - y)))$(printf '%*s' $TERM_WIDTH '')${NC}"
                    done
                    draw_sun
                    draw_dragonflies $frame
                    ;;
                4) # Dusk
                    for ((y=2; y<8; y++)); do
                        cursor_to $y 0
                        echo -ne "$(bg256 $((130 + y)))$(printf '%*s' $TERM_WIDTH '')${NC}"
                    done
                    ;;
                5) # Night
                    draw_stars
                    draw_moon
                    ;;
            esac

            # Weather effects
            draw_weather

            # Environment
            draw_reeds $frame
            draw_pond $frame
            draw_lilypad $((TERM_WIDTH/2 - 7)) $((TERM_HEIGHT - 10)) $frame

            # Flies
            draw_flies $frame

            # Eli doing froggy things
            ELI_X=$((TERM_WIDTH/2 - 5))
            ELI_Y=$((TERM_HEIGHT - 14))

            case $tod in
                0) draw_eli "sleeping" $frame ;;
                1) draw_eli "happy" $frame ;;
                2) draw_eli "eating" $frame ;;
                3) draw_eli "singing" $frame ;;
                4) draw_eli "love" $frame ;;
                5) draw_eli "sleeping" $frame ;;
            esac

            # Particles
            draw_particles
            update_particles

            # HUD
            draw_hud

            sleep 0.02
        done
    done
}

# Scene: Romance subplot
scene_romance() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_MAGENTA}═══ CHAPTER 6 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}LOVE BY THE POND${NC}"
    sleep 0.2

    clear

    ELI_X=$((TERM_WIDTH/2 - 20))
    ELI_Y=12

    for ((frame=0; frame<80; frame++)); do
        clear

        # Moonlit scene
        draw_stars
        draw_moon
        draw_pond $frame

        # Eli
        draw_eli "love" $frame

        # Love interest (Lily the frog)
        local lily_x=$((TERM_WIDTH/2 + 10))
        local lily_y=12

        cursor_to $lily_y $lily_x
        echo -ne "$(color256 213)   @${C_BRIGHT_MAGENTA}♥♥${NC}$(color256 213)@   ${NC}"
        cursor_to $((lily_y + 1)) $lily_x
        echo -ne "$(color256 213)  (${C_BRIGHT_MAGENTA}´∀\`${NC}$(color256 213))  ${NC}"
        cursor_to $((lily_y + 2)) $lily_x
        echo -ne "$(color256 207) ( >__< ) ${NC}"
        cursor_to $((lily_y + 3)) $lily_x
        echo -ne "$(color256 207)  ^    ^  ${NC}"

        # Floating hearts between them
        if ((frame % 5 == 0)); then
            for ((h=0; h<5; h++)); do
                add_particle $((TERM_WIDTH/2 - 5 + RANDOM % 10)) $((10 + RANDOM % 5)) "♥" "${C_BRIGHT_RED}" $((RANDOM % 10 + 5)) 0 -1
            done
        fi

        draw_particles
        update_particles

        # Dialogue
        if ((frame > 5 && frame < 12)); then
            cursor_to 5 $((TERM_WIDTH/2 - 15))
            echo -ne "${C_BRIGHT_GREEN}Eli: 'Ribbit... you're beautiful'${NC}"
        elif ((frame > 12 && frame < 20)); then
            cursor_to 5 $((TERM_WIDTH/2 - 15))
            echo -ne "${C_BRIGHT_MAGENTA}Lily: 'Ribbit ribbit~ ♥'${NC}"
        elif ((frame > 20)); then
            cursor_to 5 $((TERM_WIDTH/2 - 10))
            echo -ne "${C_BRIGHT_YELLOW}♫ RIBBIT DUET ♫${NC}"
        fi

        sleep 0.03
    done
}

# Scene: Boss battle
scene_boss_battle() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_RED}═══ CHAPTER 7 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}THE GREAT HERON${NC}"
    sleep 0.2

    # Warning!
    for ((flash=0; flash<10; flash++)); do
        clear
        if ((flash % 2 == 0)); then
            cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - 10))
            echo -ne "${C_BRIGHT_RED}⚠ WARNING! ⚠${NC}"
            cursor_to $((TERM_HEIGHT/2 + 2)) $((TERM_WIDTH/2 - 15))
            echo -ne "${C_BRIGHT_RED}A WILD HERON APPEARS!${NC}"
        fi
        sleep 0.05
    done

    BOSS_HEALTH=100
    ELI_X=20
    ELI_Y=$((TERM_HEIGHT - 12))

    local boss_x=$((TERM_WIDTH - 30))
    local boss_y=8

    # Battle loop
    for ((frame=0; frame<200 && BOSS_HEALTH > 0; frame++)); do
        clear

        # Battle arena
        draw_pond $frame

        # Draw boss
        draw_boss $boss_x $boss_y $frame

        # Boss attack pattern
        if ((frame % 30 < 5)); then
            # Boss diving attack
            boss_y=$((boss_y + 2))
            ((boss_y > TERM_HEIGHT - 15)) && boss_y=8

            # Check if boss hits Eli
            if ((boss_y > ELI_Y - 3 && boss_x < ELI_X + 15)); then
                HEALTH=$((HEALTH - 10))
                draw_eli "scared" $frame
                explosion ${ELI_X} ${ELI_Y}
            fi
        else
            boss_y=8
        fi

        # Eli's counter attack (every 10 frames)
        if ((frame % 10 == 0)); then
            BOSS_HEALTH=$((BOSS_HEALTH - 5))
            # Tongue attack visual
            cursor_to ${ELI_Y} $((ELI_X + 10))
            echo -ne "${C_BRIGHT_RED}━━━━━━━━━━●${NC}"
            explosion $boss_x $((boss_y + 3))
            draw_eli "angry" $frame
        else
            # Eli dodging
            if ((frame % 3 == 0)); then
                ELI_X=$((20 + RANDOM % 20))
            fi
            draw_eli "happy" $frame
        fi

        draw_particles
        update_particles

        # Health check
        if ((HEALTH <= 0)); then
            draw_eli "dead" $frame
            cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - 10))
            echo -ne "${C_BRIGHT_RED}GAME OVER${NC}"
            sleep 0.2
            HEALTH=100  # Respawn for story
            break
        fi

        sleep 0.02
    done

    # Victory!
    if ((BOSS_HEALTH <= 0)); then
        for ((v=0; v<30; v++)); do
            clear
            cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - 10))
            echo -ne "${C_BRIGHT_YELLOW}✨ VICTORY! ✨${NC}"

            explosion $((TERM_WIDTH/2 + RANDOM % 20 - 10)) $((TERM_HEIGHT/2 + RANDOM % 10 - 5))
            draw_particles
            update_particles

            sleep 0.03
        done

        SCORE=$((SCORE + 10000))
    fi
}

# Scene: The Frog Kingdom
scene_frog_kingdom() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_YELLOW}═══ CHAPTER 8 ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_WHITE}THE FROG KINGDOM${NC}"
    sleep 0.2

    # Epic reveal
    for ((frame=0; frame<100; frame++)); do
        clear

        # Castle in background
        cursor_to 3 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 28)           ▄▄████▄▄           ${NC}"
        cursor_to 4 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 28)         ▄████████████▄       ${NC}"
        cursor_to 5 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 34)        █████████████████     ${NC}"
        cursor_to 6 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 34)     ▄▄██████████████████▄▄   ${NC}"
        cursor_to 7 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 40)    ████████████████████████  ${NC}"
        cursor_to 8 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 40)    ████  ████████████  ████  ${NC}"
        cursor_to 9 $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 46)    ████  ████  ████  ████  ${NC}"

        # Frog citizens
        for ((f=0; f<8; f++)); do
            local fx=$((10 + f * 12))
            local fy=$((TERM_HEIGHT - 8))
            cursor_to $fy $fx
            if (((frame + f) % 4 < 2)); then
                echo -ne "$(color256 $((34 + f % 4))) @..@ ${NC}"
                cursor_to $((fy + 1)) $fx
                echo -ne "$(color256 $((34 + f % 4)))(^▽^)${NC}"
            else
                echo -ne "$(color256 $((34 + f % 4))) @^^@ ${NC}"
                cursor_to $((fy + 1)) $fx
                echo -ne "$(color256 $((34 + f % 4)))(°▽°)${NC}"
            fi
        done

        # King Eli on throne
        ELI_X=$((TERM_WIDTH/2 - 5))
        ELI_Y=12

        # Crown
        cursor_to 11 $((ELI_X + 2))
        echo -ne "${C_BRIGHT_YELLOW}♕${NC}"

        draw_eli "cool" $frame

        # Celebration particles
        if ((frame % 3 == 0)); then
            sparkle $((RANDOM % TERM_WIDTH)) $((RANDOM % (TERM_HEIGHT - 10) + 3))
        fi

        draw_particles
        update_particles

        # Crowd cheering
        cursor_to $((TERM_HEIGHT - 4)) $((TERM_WIDTH/2 - 15))
        local cheers=("RIBBIT!" "LONG LIVE KING ELI!" "RIBBIT RIBBIT!" "ALL HAIL THE FROG KING!")
        echo -ne "${C_BRIGHT_GREEN}${cheers[$((frame / 25 % 4))]}${NC}"

        sleep 0.02
    done
}

# Scene: The Frog Song (Musical Number)
scene_frog_song() {
    transition_fade "out"
    clear

    cursor_to 3 $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_MAGENTA}═══ MUSICAL NUMBER ═══${NC}"
    cursor_to 5 $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_WHITE}♫ THE FROG SONG ♫${NC}"
    sleep 0.2

    local lyrics=(
        "🎵 I used to be a human, working nine to five 🎵"
        "🎵 But now I'm just a froggy, feeling so alive! 🎵"
        "🎵 RIBBIT RIBBIT, that's my song 🎵"
        "🎵 Sitting on my lilypad all day long! 🎵"
        "🎵 Catching flies with my tongue so quick 🎵"
        "🎵 Being a frog is pretty slick! 🎵"
        "🎵 RIBBIT RIBBIT RIBBIT RIBBIIIIT! 🎵"
        "🎵 ELI IS A FROG AND THAT'S LEGIT! 🎵"
    )

    for ((l=0; l<${#lyrics[@]}; l++)); do
        for ((frame=0; frame<30; frame++)); do
            clear

            # Stage lights
            for ((light=0; light<10; light++)); do
                cursor_to 0 $((light * (TERM_WIDTH / 10)))
                if (((frame + light) % 3 == 0)); then
                    echo -ne "$(color256 $((196 + light % 6)))▼${NC}"
                else
                    echo -ne "$(color256 $((226 + light % 6)))▼${NC}"
                fi
            done

            # Disco floor
            for ((y=TERM_HEIGHT-5; y<TERM_HEIGHT; y++)); do
                cursor_to $y 0
                for ((x=0; x<TERM_WIDTH; x++)); do
                    if (((x + y + frame) % 4 == 0)); then
                        echo -ne "$(color256 $((196 + (x * y + frame) % 60)))█${NC}"
                    else
                        echo -ne "$(color256 $((232 + (x + y) % 10)))░${NC}"
                    fi
                done
            done

            # Dancing frogs
            for ((f=0; f<5; f++)); do
                local fx=$((10 + f * 18))
                local fy=$((TERM_HEIGHT - 10 - (frame % 4)))

                cursor_to $fy $fx
                if (((frame + f) % 4 < 2)); then
                    echo -ne "$(color256 $((46 + f * 2))) @◕◕@ ${NC}"
                    cursor_to $((fy + 1)) $fx
                    echo -ne "$(color256 $((46 + f * 2)))\\(°▽°)/${NC}"
                else
                    echo -ne "$(color256 $((46 + f * 2))) @^^@ ${NC}"
                    cursor_to $((fy + 1)) $fx
                    echo -ne "$(color256 $((46 + f * 2)))/(^▽^)\\${NC}"
                fi
            done

            # Current lyric
            cursor_to 8 $((TERM_WIDTH/2 - ${#lyrics[$l]}/2))
            echo -ne "${C_BRIGHT_YELLOW}${lyrics[$l]}${NC}"

            # Music notes floating
            if ((frame % 2 == 0)); then
                add_particle $((RANDOM % TERM_WIDTH)) $((TERM_HEIGHT - 12)) "♪" "${C_BRIGHT_MAGENTA}" 15 $((RANDOM % 3 - 1)) -1
                add_particle $((RANDOM % TERM_WIDTH)) $((TERM_HEIGHT - 12)) "♫" "${C_BRIGHT_CYAN}" 15 $((RANDOM % 3 - 1)) -1
            fi

            draw_particles
            update_particles

            sleep 0.06
        done
    done
}

# Grand finale
scene_finale() {
    transition_fade "out"
    clear

    # Epic ending sequence
    cursor_to $((TERM_HEIGHT/2 - 5)) $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_YELLOW}AND SO...${NC}"
    sleep 0.3

    cursor_to $((TERM_HEIGHT/2 - 3)) $((TERM_WIDTH/2 - 25))
    echo -ne "${C_BRIGHT_GREEN}Eli lived happily ever after as a frog.${NC}"
    sleep 0.2

    cursor_to $((TERM_HEIGHT/2 - 1)) $((TERM_WIDTH/2 - 30))
    echo -ne "${C_CYAN}He ruled the Frog Kingdom with wisdom and grace.${NC}"
    sleep 0.2

    cursor_to $((TERM_HEIGHT/2 + 1)) $((TERM_WIDTH/2 - 25))
    echo -ne "${C_BRIGHT_MAGENTA}He married Lily and had many tadpoles.${NC}"
    sleep 0.2

    cursor_to $((TERM_HEIGHT/2 + 3)) $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_WHITE}And he never filed another spreadsheet.${NC}"
    sleep 0.2

    # Final shot
    clear
    ELI_X=$((TERM_WIDTH/2 - 5))
    ELI_Y=$((TERM_HEIGHT/2 - 2))

    for ((frame=0; frame<50; frame++)); do
        clear

        # Sunset background
        for ((y=0; y<TERM_HEIGHT; y++)); do
            cursor_to $y 0
            local color=$((220 - y * 2))
            ((color < 52)) && color=52
            echo -ne "$(bg256 $color)$(printf '%*s' $TERM_WIDTH '')${NC}"
        done

        # Silhouette of Eli on lilypad
        draw_lilypad $((TERM_WIDTH/2 - 7)) $((TERM_HEIGHT - 8)) $frame
        draw_eli "happy" $frame

        # Peaceful particles
        if ((frame % 5 == 0)); then
            add_particle $((RANDOM % TERM_WIDTH)) 0 "✨" "${C_BRIGHT_YELLOW}" 20 0 1
        fi

        draw_particles
        update_particles

        sleep 0.03
    done

    # THE END
    clear
    for ((glow=0; glow<30; glow++)); do
        clear

        cursor_to $((TERM_HEIGHT/2 - 3)) $((TERM_WIDTH/2 - 20))
        echo -ne "$(color256 $((46 + glow % 10)))"
        cat << 'EOF'
 ████████╗██╗  ██╗███████╗    ███████╗███╗   ██╗██████╗
 ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝████╗  ██║██╔══██╗
    ██║   ███████║█████╗      █████╗  ██╔██╗ ██║██║  ██║
    ██║   ██╔══██║██╔══╝      ██╔══╝  ██║╚██╗██║██║  ██║
    ██║   ██║  ██║███████╗    ███████╗██║ ╚████║██████╔╝
    ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝╚═════╝
EOF
        echo -ne "${NC}"

        sparkle $((TERM_WIDTH/2)) $((TERM_HEIGHT/2))
        draw_particles
        update_particles

        sleep 0.03
    done
}

# Rolling credits
rolling_credits() {
    clear

    local credits=(
        ""
        ""
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ""
        "ELI IS A FROG"
        ""
        "THE ULTIMATE CINEMATIC EXPERIENCE"
        "DIRECTOR'S CUT EXTENDED EDITION"
        ""
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ""
        ""
        "STARRING"
        ""
        "ELI .................. as HIMSELF (as a FROG)"
        "LILY ................. as THE LOVE INTEREST"
        "THE GREAT HERON ...... as THE VILLAIN"
        "VARIOUS FLIES ........ as SNACKS"
        ""
        ""
        "DIRECTED BY"
        "A Very Ambitious Shell Script"
        ""
        ""
        "PRODUCED BY"
        "Claude Code Productions"
        ""
        ""
        "WRITTEN BY"
        "Claude (Opus 4.5)"
        ""
        ""
        "ORIGINAL SCORE"
        "Terminal Beep Symphony Orchestra"
        ""
        ""
        "VISUAL EFFECTS"
        "ANSI Escape Codes"
        "256-Color Mode"
        "Pure Bash Magic"
        ""
        ""
        "SPECIAL THANKS"
        ""
        "To all the frogs who inspired this film"
        "To lilypads everywhere"
        "To flies (sorry)"
        "To Evan for making this possible"
        ""
        ""
        "TECHNICAL SPECIFICATIONS"
        ""
        "Rendered in: Bash 4.0+"
        "Resolution: ${TERM_WIDTH}x${TERM_HEIGHT} characters"
        "Color Depth: 256 colors"
        "Frame Rate: Whatever your terminal can handle"
        "Sound: Terminal bells (so cinematic)"
        ""
        ""
        "STATISTICS"
        ""
        "Flies Eaten: ${FLIES_EATEN}"
        "Total Ribbits: ${TOTAL_RIBBITS}"
        "Maximum Combo: ${MAX_COMBO}"
        "Final Score: ${SCORE}"
        ""
        ""
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ""
        "NO FLIES WERE HARMED IN THE MAKING"
        "OF THIS FILM"
        ""
        "(they were delicious though)"
        ""
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ""
        ""
        "🐸 RIBBIT! 🐸"
        ""
        ""
        "© 2024 FROG ENTERTAINMENT"
        "ALL RIGHTS RESERVED"
        ""
        ""
        ""
        "...or are they?"
        ""
        ""
        "(yes, yes they are)"
        ""
        ""
        ""
        ""
        "Why are you still reading?"
        ""
        ""
        "The movie is over."
        ""
        ""
        "Go outside."
        ""
        ""
        "Touch some grass."
        ""
        ""
        "Maybe visit a pond."
        ""
        ""
        "Look for frogs."
        ""
        ""
        "RIBBIT."
        ""
        ""
        ""
        ""
        ""
        ""
        ""
        "🐸"
    )

    local total_lines=${#credits[@]}
    local scroll_position=0

    for ((scroll_position=0; scroll_position < total_lines + TERM_HEIGHT; scroll_position+=3)); do
        clear

        for ((screen_y=0; screen_y<TERM_HEIGHT; screen_y++)); do
            local credit_line=$((scroll_position - TERM_HEIGHT + screen_y))
            if ((credit_line >= 0 && credit_line < total_lines)); then
                local line="${credits[$credit_line]}"
                local x=$(( (TERM_WIDTH - ${#line}) / 2 ))
                ((x < 0)) && x=0
                cursor_to $screen_y $x

                # Color based on content
                if [[ "$line" == *"━"* ]]; then
                    echo -ne "${C_BRIGHT_GREEN}${line}${NC}"
                elif [[ "$line" == *"STARRING"* ]] || [[ "$line" == *"DIRECTED"* ]] || [[ "$line" == *"PRODUCED"* ]] || [[ "$line" == *"WRITTEN"* ]] || [[ "$line" == *"SPECIAL"* ]] || [[ "$line" == *"TECHNICAL"* ]] || [[ "$line" == *"STATISTICS"* ]]; then
                    echo -ne "${C_BRIGHT_YELLOW}${line}${NC}"
                elif [[ "$line" == *"ELI IS A FROG"* ]]; then
                    echo -ne "${C_BRIGHT_GREEN}${line}${NC}"
                elif [[ "$line" == *"RIBBIT"* ]] || [[ "$line" == *"🐸"* ]]; then
                    echo -ne "${C_BRIGHT_GREEN}${line}${NC}"
                else
                    echo -ne "${C_WHITE}${line}${NC}"
                fi
            fi
        done

        # Frog decorations on sides
        if ((scroll_position % 10 < 5)); then
            cursor_to $((TERM_HEIGHT - 5)) 5
            echo -ne "${C_BRIGHT_GREEN}@..@${NC}"
            cursor_to $((TERM_HEIGHT - 4)) 5
            echo -ne "${C_BRIGHT_GREEN}(°▽°)${NC}"

            cursor_to $((TERM_HEIGHT - 5)) $((TERM_WIDTH - 10))
            echo -ne "${C_BRIGHT_GREEN}@..@${NC}"
            cursor_to $((TERM_HEIGHT - 4)) $((TERM_WIDTH - 10))
            echo -ne "${C_BRIGHT_GREEN}(°▽°)${NC}"
        else
            cursor_to $((TERM_HEIGHT - 5)) 5
            echo -ne "${C_BRIGHT_GREEN}@^^@${NC}"
            cursor_to $((TERM_HEIGHT - 4)) 5
            echo -ne "${C_BRIGHT_GREEN}(^▽^)${NC}"

            cursor_to $((TERM_HEIGHT - 5)) $((TERM_WIDTH - 10))
            echo -ne "${C_BRIGHT_GREEN}@^^@${NC}"
            cursor_to $((TERM_HEIGHT - 4)) $((TERM_WIDTH - 10))
            echo -ne "${C_BRIGHT_GREEN}(^▽^)${NC}"
        fi

        sleep 0.02
    done
}

# Post-credits scene
post_credits() {
    sleep 0.3
    clear

    cursor_to $((TERM_HEIGHT/2 - 2)) $((TERM_WIDTH/2 - 15))
    echo -ne "${C_DIM}[POST-CREDITS SCENE]${NC}"
    sleep 0.2

    clear

    # Dark office scene
    cursor_to 5 10
    echo -ne "${C_DIM}╔════════════════════════════════════╗${NC}"
    cursor_to 6 10
    echo -ne "${C_DIM}║   ACME CORPORATION - CUBICLE 42   ║${NC}"
    cursor_to 7 10
    echo -ne "${C_DIM}╚════════════════════════════════════╝${NC}"

    # Empty desk
    cursor_to 15 20
    echo -ne "${C_YELLOW}┌──────────────────────┐${NC}"
    cursor_to 16 20
    echo -ne "${C_YELLOW}│ ${C_DIM}[____] ${C_CYAN}☕ ${C_DIM}📄 📊${C_YELLOW}     │${NC}"
    cursor_to 17 20
    echo -ne "${C_YELLOW}└──────────────────────┘${NC}"

    sleep 0.2

    # Note on desk
    cursor_to 14 25
    echo -ne "${C_WHITE}📝${NC}"

    cursor_to 20 15
    typewriter "Note: 'Gone to be a frog. Don't wait up. - Eli'" 20 15 0.05

    sleep 0.3

    # Small frog hopping away
    for ((hop=0; hop<15; hop++)); do
        cursor_to 12 $((50 + hop * 3))
        if ((hop % 2 == 0)); then
            echo -ne "${C_BRIGHT_GREEN}@..@  ${NC}"
        else
            echo -ne "      "
        fi
        sleep 0.05
    done

    cursor_to 12 $((50 + 15 * 3))
    echo -ne "${C_BRIGHT_GREEN}ribbit!${NC}"

    sleep 0.2

    # FROG WILL RETURN
    clear
    cursor_to $((TERM_HEIGHT/2)) $((TERM_WIDTH/2 - 15))
    echo -ne "${C_BRIGHT_GREEN}ELI WILL RETURN${NC}"
    cursor_to $((TERM_HEIGHT/2 + 2)) $((TERM_WIDTH/2 - 10))
    echo -ne "${C_DIM}in${NC}"
    cursor_to $((TERM_HEIGHT/2 + 4)) $((TERM_WIDTH/2 - 20))
    echo -ne "${C_BRIGHT_YELLOW}ELI IS A FROG 2: ELECTRIC RIBBIT${NC}"

    sleep 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    # Initialize
    hide_cursor
    clear

    # Initialize systems
    init_stars
    init_rain
    init_flies

    # Run the movie!
    title_screen
    scene_normal_life
    scene_discovery
    scene_transformation
    scene_frog_training
    scene_day_in_life
    scene_romance
    scene_boss_battle
    scene_frog_kingdom
    scene_frog_song
    scene_finale
    rolling_credits
    post_credits

    # Final cleanup happens in trap
}

# Run it!
main
