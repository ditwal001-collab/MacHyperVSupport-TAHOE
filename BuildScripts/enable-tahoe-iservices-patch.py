"""Enable an existing paired OpenCore VM-detection workaround in a NEW plist.

Does not access a VM, disk image, account or network. No identity/policy edits.
Upstream: Qonfused/OSX-Hyper-V a377f97; see its e689108 follow-up.
This is a VM-detection compatibility workaround, not native Apple attestation.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import plistlib

FIND_A = b'hibernatehidready\0hibernatecount\0'
REPLACE_A = b'hibernatehidready\0hv_vmm_present\0'
FIND_B = b'boot session UUID\0hv_vmm_present\0'
REPLACE_B = b'boot session UUID\0hibernatecount\0'


def checked(original):
    patches = original['Kernel']['Patch']
    companions = [p for p in patches if p.get('Identifier') == 'kernel'
                  and p.get('Find') == FIND_A and p.get('Replace') == REPLACE_A]
    targets = [(i, p) for i, p in enumerate(patches) if p.get('Identifier') == 'kernel'
               and p.get('Find') == FIND_B and p.get('Replace') == REPLACE_B]
    if len(companions) != 1 or companions[0].get('Enabled') is not True:
        raise ValueError('Expected exactly one enabled upstream companion patch')
    companion = companions[0]
    if companion.get('Arch') != 'x86_64' or companion.get('MinKernel') != '20.4.0' or companion.get('MaxKernel'):
        raise ValueError('Unexpected companion architecture or kernel bounds')
    if len(targets) != 1:
        raise ValueError('Expected exactly one existing upstream target patch')
    index, target = targets[0]
    if target.get('Arch') != 'x86_64' or target.get('MinKernel') != '22.0.0' or target.get('MaxKernel'):
        raise ValueError('Unexpected target architecture or kernel bounds')
    if not isinstance(target.get('Enabled'), bool):
        raise ValueError('Target activation must be a boolean')
    for patch in (companion, target):
        for key, empty in (('Base', ''), ('Mask', b''), ('ReplaceMask', b''), ('Skip', 0), ('Limit', 0)):
            if patch.get(key, empty) != empty:
                raise ValueError('Unexpected patch control: ' + key)
        if patch.get('Count', 0) not in (0, 1):
            raise ValueError('Unexpected patch count')
    return index, target['Enabled']


def corrected(original):
    index, enabled = checked(original)
    if enabled:
        raise ValueError('Target is not disabled; refusing an unneeded change')
    result = copy.deepcopy(original)
    target = result['Kernel']['Patch'][index]
    target['Enabled'] = True
    check = copy.deepcopy(result)
    check['Kernel']['Patch'][index]['Enabled'] = False
    assert check == original, 'Unexpected non-target change'
    return result, index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--expected-sha256', required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', action='store_true', help='Read-only pair validation, no output file')
    args = parser.parse_args()
    data = args.config.read_bytes()
    before = hashlib.sha256(data).hexdigest()
    if before != args.expected_sha256.lower():
        raise SystemExit('Source config hash mismatch')
    original = plistlib.loads(data)
    if args.check:
        index, enabled = checked(original)
        print(json.dumps({'config_sha256': before, 'target_index': index,
                          'pair_enabled': enabled, 'valid_pair': True}, indent=2))
        return
    result, index = corrected(original)
    output = plistlib.dumps(result, fmt=plistlib.FMT_XML, sort_keys=False)
    # Exclusive create: never overwrite source or any previous result/backup.
    with args.output.open('xb') as destination:
        destination.write(output)
    assert plistlib.loads(args.output.read_bytes()) == result
    print(json.dumps({'before_sha256': before,
                      'after_sha256': hashlib.sha256(output).hexdigest(),
                      'changed_key': 'Kernel.Patch.' + str(index) + '.Enabled',
                      'before': False, 'after': True,
                      'scope': 'one existing flag only; all other plist values preserved'}, indent=2))


if __name__ == '__main__':
    main()
