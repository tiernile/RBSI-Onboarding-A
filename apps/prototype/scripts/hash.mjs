import bcrypt from 'bcryptjs'

const pw = process.argv[2]
if (!pw) {
  console.error('Usage: pnpm hash "YourPassword"')
  process.exit(1)
}
const rounds = 12
const salt = bcrypt.genSaltSync(rounds)
const hash = bcrypt.hashSync(pw, salt)
console.log(hash)

