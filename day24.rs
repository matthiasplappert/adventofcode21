// stolen from https://github.com/Mahrgell/AoC2021/blob/main/aoc21-24/src/main.rs
use std::collections::HashMap;
use std::fs;

#[derive(Clone, Copy, Debug)]
enum Val {
    Dyn(usize),
    Fixed(i64),
}

#[derive(Clone, Copy, Debug)]
enum Op {
    Inp(usize),
    Add(usize, Val),
    Mul(usize, Val),
    Div(usize, Val),
    Mod(usize, Val),
    Eql(usize, Val),
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct Alu {
    mem: [i64; 4],
}

fn variable_to_index(s: &str) -> Option<usize> {
    match s {
        "w" => Some(0),
        "x" => Some(1),
        "y" => Some(2),
        "z" => Some(3),
        _ => None,
    }
}

impl Op {
    fn from_line(l: &str) -> Self {
        let words: Vec<_> = l.split(' ').collect();
        let target = variable_to_index(words[1]).unwrap();
        let val = if words.len() < 3 {
            Val::Fixed(0)
        } else {
            if let Some(idx) = variable_to_index(words[2]) {
                Val::Dyn(idx)
            } else {
                Val::Fixed(words[2].parse::<i64>().unwrap())
            }
        };
        match words[0] {
            "inp" => Op::Inp(target),
            "add" => Op::Add(target, val),
            "mul" => Op::Mul(target, val),
            "div" => Op::Div(target, val),
            "mod" => Op::Mod(target, val),
            "eql" => Op::Eql(target, val),
            _ => panic!(),
        }
    }
}

impl Alu {
    fn apply_op(&mut self, op: Op) {
        match op {
            Op::Inp(_) => panic!(),
            Op::Add(l, v) => self.mem[l] += self.get_val(v),
            Op::Mul(l, v) => self.mem[l] *= self.get_val(v),
            Op::Div(l, v) => self.mem[l] /= self.get_val(v),
            Op::Mod(l, v) => self.mem[l] %= self.get_val(v),
            Op::Eql(l, v) => self.mem[l] = (self.mem[l] == self.get_val(v)) as i64,
        }
    }

    fn apply_inp(&mut self, target: usize, val: i64) {
        self.mem[target] = val;
    }

    fn get_val(&self, v: Val) -> i64 {
        match v {
            Val::Dyn(i) => self.mem[i],
            Val::Fixed(f) => f,
        }
    }
}

fn main() {
    let contents = fs::read_to_string("day24.txt").expect("Failed to read file.");
    let ops: Vec<_> = contents.lines().map(|l| Op::from_line(l)).collect();

    let mut alus: Vec<(Alu, (u64, u64))> = vec![(Alu { mem: [0; 4] }, (0, 0))];
    for op in ops {
        match op {
            Op::Inp(t) => {
                let mut new_alus: Vec<(Alu, (u64, u64))> = Vec::new();
                let mut indizes: HashMap<Alu, usize> = HashMap::new();
                for alu in &alus {
                    for v in 1..=9 {
                        let mut new_alu = alu.clone();
                        new_alu.0.apply_inp(t, v);
                        new_alu.1 .0 = new_alu.1 .0 * 10 + v as u64;
                        new_alu.1 .1 = new_alu.1 .1 * 10 + v as u64;
                        if let Some(idx) = indizes.get(&new_alu.0) {
                            new_alus[*idx].1 .0 = u64::min(new_alus[*idx].1 .0, new_alu.1 .0);
                            new_alus[*idx].1 .1 = u64::max(new_alus[*idx].1 .1, new_alu.1 .1);
                        } else {
                            indizes.insert(new_alu.0.clone(), new_alus.len());
                            new_alus.push(new_alu);
                        }
                    }
                }
                alus = new_alus;
                println!("Processing {} alu states.", alus.len());
            }
            op => {
                for alu in &mut alus {
                    alu.0.apply_op(op);
                }
            }
        }
    }
    let mut lowest = u64::MAX;
    let mut highest = u64::MIN;
    for alu in &alus {
        if alu.0.mem[3] == 0 {
            lowest = u64::min(lowest, alu.1 .0);
            highest = u64::max(highest, alu.1 .1);
        }
    }
    println!("Highest input: {}", highest);
    println!("Lowest input: {}", lowest);
}