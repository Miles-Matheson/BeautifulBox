//
//  HomeCell.m
//  BeautifulBox
//
//  Created by Miles on 17/2/14.
//  Copyright © 2017年 Miles. All rights reserved.
//

#import "HomeCell.h"

@interface HomeCell ()
@property (nonatomic,strong)UIImageView *headImgView;
@property (nonatomic,strong)UILabel *nameLab;

@end


@implementation HomeCell

- (void)awakeFromNib {
    [super awakeFromNib];
    // Initialization code
}


- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier
{
    if (self = [super initWithStyle:style reuseIdentifier:reuseIdentifier]) {
        self.headImgView = [[UIImageView alloc]initWithFrame:CGRectMake(5, 5, 20, 20)];
        self.headImgView.backgroundColor = [UIColor grayColor];
        
        [self.contentView addSubview:self.headImgView];
        
        
        self.nameLab = [[UILabel alloc]initWithFrame:CGRectMake(5, 5, 20, 20)];
        self.nameLab.text = self.titleName;
        self.nameLab.font = [UIFont systemFontOfSize:11];
        [self.contentView addSubview:self.nameLab];
    }

  
    return self;
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated {
    [super setSelected:selected animated:animated];

    
    

      
}

- (void)layoutSubviews
{
    [super layoutSubviews];
   
    [self.headImgView sd_setImageWithURL:[NSURL URLWithString:self.imageName] placeholderImage:[UIImage imageNamed:@""]];
    if (_nameLab) {
        self.nameLab.text = self.titleName;
         [self.nameLab sizeToFit];
        self.nameLab.centerY = self.headImgView.centerY;
        self.nameLab.left = self.headImgView.right+5;
    }
    
}

@end
